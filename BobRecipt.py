import json
import time

import requests
from bs4 import BeautifulSoup

from db.database import get_db
from services.save_recipe import save_recipe
from services.save_recipe_detail import save_recipe_details
from services.save_recipe_detail_ingredients import save_recipe_detail_ingredients
from services.save_recipe_ingredients import save_recipe_ingredients


def get_recipe_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Recipe {url} not found or inaccessible.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # 레시피 정보가 없을 경우 빈 값 리턴
    if soup.find("script", text=lambda t: t and "레시피 정보가 없습니다" in t):
        print(f"Recipe {url} is not available (missing recipe alert detected).")
        return None

    # 레시피 제목
    title = soup.select_one('div.view2_summary h3').text.strip()

    # 레시피 이미지
    image = soup.select('.centeredcrop img')[0]['src']

    # 레시피 설명
    description = soup.select_one('div.view2_summary_in').text.strip()

    # 인원수, 시간, 난이도
    info_section = soup.select('div.view2_summary_info span')
    servings = info_section[0].text.strip()  # ex) '3인분'
    if len(info_section) > 1:
        cooking_time = info_section[1].text.strip()  # ex) '30분 이내'
    else:
        cooking_time = ""
    if len(info_section) > 2:
        difficulty = info_section[2].text.strip()  # ex) '초급'
    else:
        difficulty = ""

    # 재료 목록 크롤링
    ingredients_section = soup.select('div.ready_ingre3 ul li')
    ingredients = []  # 재료 목록 + 양념
    for ingredient in ingredients_section:
        name = ingredient.select_one('a').text.strip()
        if name == "구매":
            continue
        volume = ingredient.select_one('span').text.strip()
        amount = ingredient.select_one('b').text.strip() if ingredient.select_one('b') else '적당량'
        ingredients.append({
            'name': name,
            'volume': volume,
            'amount': amount
        })

    # 요리 단계 크롤링
    steps = soup.select('.view_step_cont')
    images = soup.select('.view_step_cont img')

    recipe_steps = []
    ingredient_names = [ing['name'] for ing in ingredients]  # 재료 이름 리스트

    for index, step in enumerate(steps):
        step_text = step.text.strip()
        step_image = images[index]['src'] if index < len(images) else None

        # step_text를 공백으로 나누어 재료와 일치하는 단어 찾기
        step_words = step_text.split()
        matching_ingredients = [name for name in ingredient_names if any(name in word for word in step_words)]

        recipe_steps.append({
            'step_number': index + 1,
            'description': step_text,
            'image_url': step_image,
            'ingredient_list': matching_ingredients  # 해당 단계에 사용된 재료
        })

    # 결과를 딕셔너리로 정리
    recipe_data = {
        'title': title,
        'image': image,
        'description': description,
        'servings': servings,
        'cooking_time': cooking_time,
        'difficulty': difficulty,
        'ingredients': ingredients,
        'steps': recipe_steps
    }

    return recipe_data


# 데이터 저장 로직
def save_crawled_recipe(recipe_data, url):
    db = next(get_db())
    """
    Save crawled recipe data into the database.
    """
    try:
        # Ensure recipe_data is a dictionary
        if isinstance(recipe_data, str):  # If recipe_data is a JSON string
            recipe_data = json.loads(recipe_data)  # Convert to dictionary

        # Save main recipe
        recipe_id = save_recipe(db, recipe_data, url)

        # Save ingredients
        save_recipe_ingredients(db, recipe_id, recipe_data["ingredients"])

        # Save recipe details
        recipe_details = save_recipe_details(db, recipe_id, recipe_data["steps"])

        # Save ingredients for each recipe step
        for recipe_detail_id, ingredient_list in recipe_details:
            save_recipe_detail_ingredients(db, recipe_detail_id, ingredient_list)

        print(f"Recipe '{recipe_data['title']}' saved successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error occurred while saving recipe: {e}")
    finally:
        db.close()


# 레시피 ID 입력
start_id = 7000043
end_id = 7000045  # 테스트 범위로 변경, 실제는 8000000

for recipe_id in range(start_id, end_id):
    url = f'https://www.10000recipe.com/recipe/{recipe_id}'
    try:
        recipe_data = get_recipe_details(url)
        if recipe_data:
            print(json.dumps(recipe_data, ensure_ascii=False, indent=4))
            # try:
            #     save_crawled_recipe(json.dumps(recipe_data, ensure_ascii=False, indent=4), url)
            #     print(f"Recipe {recipe_id} saved successfully.")
            # except Exception as e:
            #     print(f"Error occurred while saving recipe(id={recipe_id}): {e}")
            #     break
        else:
            print(f"Skipping Recipe {recipe_id}.")
    except Exception as e:
        print(f"Error occurred while read recipe(id={recipe_id}): {e}")
        break

    time.sleep(2)  # 2초 대기
