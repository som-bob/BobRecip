from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

# 1. BobRecipe (레시피 테이블)
class BobRecipe(Base):
    __tablename__ = "bob_recipe"

    recipe_id = Column(Integer, primary_key=True, autoincrement=True, comment="레시피 ID")
    recipe_name = Column(String(200), nullable=False, comment="레시피명")
    recipe_description = Column(String(1000), comment="레시피 설명")
    servings = Column(String(50), comment="몇 인분 정보")
    difficulty = Column(String(20), comment="난이도")
    cooking_time = Column(Integer, comment="소요 시간 (분)")
    source = Column(String(255), comment="출처 URL 또는 출처 정보")
    image_url = Column(String(255), comment="대표 이미지 URL")
    reg_id = Column(String(100), nullable=False, comment="글쓴이 이메일")
    reg_date = Column(DateTime, default=datetime.datetime.utcnow, comment="등록 날짜")
    mod_id = Column(String(100), comment="수정자 이메일")
    mod_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, comment="수정 날짜")

    # Relationships
    details = relationship("BobRecipeDetail", back_populates="recipe", cascade="all, delete-orphan")
    recipe_ingredients = relationship("BobRecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")


# 2. BobRecipeDetail (레시피 상세 테이블)
class BobRecipeDetail(Base):
    __tablename__ = "bob_recipe_detail"

    recipe_detail_id = Column(Integer, primary_key=True, autoincrement=True, comment="레시피 상세 ID")
    recipe_id = Column(Integer, ForeignKey("bob_recipe.recipe_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, comment="레시피 ID (FK)")
    image_url = Column(String(255), comment="레시피 상세 이미지 URL")
    recipe_order = Column(Integer, nullable=False, comment="조리 순서")
    recipe_detail_text = Column(String(3000), comment="레시피 상세 텍스트")
    reg_id = Column(String(100), nullable=False, comment="글쓴이 이메일")
    reg_date = Column(DateTime, default=datetime.datetime.utcnow, comment="등록 날짜")
    mod_id = Column(String(100), comment="수정자 이메일")
    mod_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, comment="수정 날짜")

    # Relationships
    recipe = relationship("BobRecipe", back_populates="details")
    detail_ingredients = relationship("BobRecipeDetailIngredient", back_populates="recipe_detail", cascade="all, delete-orphan")


# 3. BobRecipeDetailIngredient (레시피 상세 재료 테이블)
class BobRecipeDetailIngredient(Base):
    __tablename__ = "bob_recipe_detail_ingredient"

    detail_ingredient_id = Column(Integer, primary_key=True, autoincrement=True, comment="레시피 상세 재료 ID")
    recipe_detail_id = Column(Integer, ForeignKey("bob_recipe_detail.recipe_detail_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, comment="레시피 상세 ID (FK)")
    ingredient_id = Column(Integer, ForeignKey("bob_ingredients.ingredient_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, comment="재료 ID (FK)")
    reg_id = Column(String(100), nullable=False, comment="글쓴이 이메일")
    reg_date = Column(DateTime, default=datetime.datetime.utcnow, comment="등록 날짜")
    mod_id = Column(String(100), comment="수정자 이메일")
    mod_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, comment="수정 날짜")

    # Relationships
    recipe_detail = relationship("BobRecipeDetail", back_populates="detail_ingredients")
    ingredient = relationship("BobIngredient")


# 4. BobIngredient (재료 테이블)
class BobIngredient(Base):
    __tablename__ = "bob_ingredients"

    ingredient_id = Column(Integer, primary_key=True, autoincrement=True, comment="재료 ID")
    ingredient_name = Column(String(100), nullable=False, comment="재료명")
    ingredient_description = Column(String(500), comment="재료 설명")
    image_url = Column(String(255), comment="재료 이미지 URL")
    icon_url = Column(String(255), comment="재료 아이콘 URL")
    storage_method = Column(String(100), comment="보관 방법")
    storage_days = Column(Integer, comment="보관 가능 일수")
    reg_id = Column(String(100), nullable=False, comment="글쓴이 이메일")
    reg_date = Column(DateTime, default=datetime.datetime.utcnow, comment="등록 날짜")
    mod_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, comment="수정 날짜")


# 5. BobRecipeIngredient (레시피-재료 관계 테이블)
class BobRecipeIngredient(Base):
    __tablename__ = "bob_recipe_ingredients"

    detail_ingredient_id = Column(Integer, primary_key=True, autoincrement=True, comment="레시피 재료 상세 ID")
    recipe_id = Column(Integer, ForeignKey("bob_recipe.recipe_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, comment="레시피 ID (FK)")
    ingredient_id = Column(Integer, ForeignKey("bob_ingredients.ingredient_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, comment="재료 ID (FK)")
    amount = Column(String(100), comment="양 텍스트 (ex: 1/2T, 3T, 적당량 등)")
    reg_id = Column(String(100), nullable=False, comment="글쓴이 이메일")
    reg_date = Column(DateTime, default=datetime.datetime.utcnow, comment="등록 날짜")
    mod_id = Column(String(100), comment="수정자 이메일")
    mod_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, comment="수정 날짜")

    # Relationships
    recipe = relationship("BobRecipe", back_populates="recipe_ingredients")
    ingredient = relationship("BobIngredient")