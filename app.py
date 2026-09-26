from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-recipe-key'
# Use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300))
    ingredients = db.Column(db.Text, nullable=False) # Stored as JSON string
    instructions = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


def seed_recipes():
    if Recipe.query.first():
        return

    sample_recipes = [
        Recipe(
            title='Sunrise Veggie Omelet',
            description='A bright and satisfying breakfast full of herbs and vegetables.',
            ingredients=json.dumps(['2 eggs', '1/4 cup spinach', '1/4 cup tomatoes', '2 tbsp onion', '1 tbsp olive oil', 'Salt and pepper']),
            instructions='1. Heat the olive oil in a skillet.\n2. Sauté the onion and tomatoes for 2 minutes.\n3. Add spinach and cook until wilted.\n4. Pour in the beaten eggs and stir gently.\n5. Fold the omelet and cook until set.\n6. Season with salt and pepper before serving.'
        ),
        Recipe(
            title='Citrus Chicken Bowl',
            description='A fresh, protein-packed bowl with grains, greens, and a lemony finish.',
            ingredients=json.dumps(['2 chicken breasts', '1 cup cooked rice', '1 cup quinoa', '1 cup cucumber', '1/2 cup cherry tomatoes', '2 tbsp lemon juice', '1 tbsp olive oil']),
            instructions='1. Season the chicken with salt, pepper, and a little lemon juice.\n2. Pan-cook the chicken until golden and fully cooked.\n3. Slice it into strips.\n4. Arrange rice or quinoa in bowls with greens, cucumber, and tomatoes.\n5. Top with chicken and drizzle with olive oil and remaining lemon juice.'
        ),
        Recipe(
            title='Creamy Mushroom Pasta',
            description='Comfort food with a silky garlic cream sauce and earthy mushrooms.',
            ingredients=json.dumps(['200g pasta', '1 cup mushrooms', '2 garlic cloves', '1/2 cup cream', '1/4 cup parmesan', '1 tbsp butter', 'Parsley for garnish']),
            instructions='1. Cook the pasta according to package instructions.\n2. Sauté mushrooms in butter until golden.\n3. Add garlic and cook for 30 seconds.\n4. Stir in cream and parmesan until smooth.\n5. Toss in the cooked pasta and mushrooms.\n6. Garnish with parsley and serve warm.'
        ),
        Recipe(
            title='Berry Yogurt Parfait',
            description='A quick, refreshing dessert or breakfast layered with fruit and crunch.',
            ingredients=json.dumps(['1 cup Greek yogurt', '1/2 cup mixed berries', '1/4 cup granola', '1 tbsp honey', '1 tsp chia seeds']),
            instructions='1. Spoon a layer of yogurt into a glass or bowl.\n2. Add berries and a drizzle of honey.\n3. Sprinkle granola and chia seeds.\n4. Repeat the layers until full.\n5. Serve immediately or chill for a few minutes.'
        ),
        Recipe(
            title='Paneer Tikka Masala',
            description='Soft paneer cubes simmered in a rich tomato and cashew curry.',
            ingredients=json.dumps(['250g paneer', '1 cup tomato puree', '1/2 cup cream', '1 tbsp ginger-garlic paste', '1 tsp garam masala', '1 tsp chili powder', 'Fresh coriander']),
            instructions='1. Marinate paneer with spices and grill or pan-sear.\n2. Cook onion, ginger-garlic paste, and tomato puree in a pan.\n3. Add spices and simmer gently.\n4. Stir in cream and paneer.\n5. Cook until thick and glossy.\n6. Garnish with coriander and serve with naan.'
        ),
        Recipe(
            title='Chickpea Spinach Curry',
            description='A hearty, plant-based curry filled with warm spices and greens.',
            ingredients=json.dumps(['1 cup chickpeas', '2 cups spinach', '1 onion', '2 tomatoes', '1 tbsp curry powder', '1/2 cup coconut milk', 'Salt to taste']),
            instructions='1. Sauté onion until soft.\n2. Add tomatoes and curry powder and cook until jammy.\n3. Mix in chickpeas and coconut milk.\n4. Simmer for 10 minutes.\n5. Add spinach and cook until wilted.\n6. Serve with rice or flatbread.'
        ),
        Recipe(
            title='Grilled Veggie Wrap',
            description='A colorful wrap packed with roasted vegetables and hummus.',
            ingredients=json.dumps(['2 tortillas', '1 cup zucchini', '1 cup bell peppers', '1/2 cup hummus', '1/4 cup feta', 'Lettuce leaves', 'Olive oil']),
            instructions='1. Roast or grill the vegetables until tender.\n2. Warm the tortillas.\n3. Spread hummus on each tortilla.\n4. Add lettuce, roasted vegetables, and feta.\n5. Roll tightly and slice in half.'
        ),
        Recipe(
            title='Lentil Soup',
            description='A comforting, nourishing soup with lentils, carrots, and herbs.',
            ingredients=json.dumps(['1 cup red lentils', '2 carrots', '1 onion', '2 cups vegetable stock', '1 tsp cumin', '1 tbsp lemon juice', 'Salt and pepper']),
            instructions='1. Sauté onion and carrot until softened.\n2. Add lentils, cumin, and stock.\n3. Simmer until lentils are tender.\n4. Blend gently for a thicker texture if desired.\n5. Finish with lemon juice and seasoning.'
        ),
        Recipe(
            title='Garlic Butter Shrimp',
            description='Quick shrimp sautéed in garlic butter and a hint of lemon.',
            ingredients=json.dumps(['250g shrimp', '2 tbsp butter', '3 garlic cloves', '1 tbsp lemon juice', '1 tbsp parsley', 'Chili flakes', 'Salt']),
            instructions='1. Pat the shrimp dry and season lightly with salt.\n2. Melt butter with garlic until fragrant.\n3. Add shrimp and cook for 2 minutes per side.\n4. Finish with lemon juice and parsley.\n5. Serve with rice or toast.'
        ),
        Recipe(
            title='Herb Chicken Skillet',
            description='Tender chicken pieces cooked with herbs and crispy potatoes.',
            ingredients=json.dumps(['2 chicken thighs', '2 potatoes', '1 tsp rosemary', '1 tsp thyme', '2 tbsp olive oil', '1 garlic clove', 'Salt and pepper']),
            instructions='1. Cube the potatoes and parboil until slightly tender.\n2. Sear the chicken until browned.\n3. Add potatoes, garlic, and herbs.\n4. Cook until the potatoes are crisp and the chicken is done.\n5. Serve warm.'
        ),
        Recipe(
            title='Spicy Tofu Stir-Fry',
            description='Crispy tofu tossed with vegetables in a bold soy-garlic sauce.',
            ingredients=json.dumps(['200g tofu', '1 bell pepper', '1 carrot', '1 cup broccoli', '2 tbsp soy sauce', '1 tbsp sesame oil', '1 tsp chili sauce', 'Garlic']),
            instructions='1. Pan-fry tofu until crisp.\n2. Stir-fry vegetables in sesame oil.\n3. Add garlic, soy sauce, and chili sauce.\n4. Toss in tofu and cook for another minute.\n5. Serve with rice.'
        ),
        Recipe(
            title='Baked Salmon with Dill',
            description='Simple oven-roasted salmon with a fresh herb finish.',
            ingredients=json.dumps(['2 salmon fillets', '1 tbsp olive oil', '1 tbsp dill', '1 lemon', 'Salt', 'Black pepper']),
            instructions='1. Preheat the oven to 200°C.\n2. Place salmon on a lined tray and drizzle with oil.\n3. Season with dill, salt, pepper, and lemon zest.\n4. Bake for 15 to 18 minutes.\n5. Serve with greens or potatoes.'
        ),
        Recipe(
            title='Caprese Salad',
            description='A light and elegant salad of tomatoes, mozzarella, and basil.',
            ingredients=json.dumps(['2 tomatoes', '1 ball mozzarella', 'Fresh basil', '1 tbsp balsamic glaze', '1 tbsp olive oil', 'Salt']),
            instructions='1. Slice tomatoes and mozzarella.\n2. Layer them alternately with basil leaves.\n3. Drizzle with olive oil and balsamic glaze.\n4. Season with salt and serve immediately.'
        ),
        Recipe(
            title='Matar Paneer',
            description='Green peas and paneer cooked in a fragrant spiced gravy.',
            ingredients=json.dumps(['250g paneer', '1 cup peas', '1 onion', '2 tomatoes', '1 tsp turmeric', '1 tsp cumin', '1 tsp coriander']),
            instructions='1. Sauté onion and tomatoes until soft.\n2. Add turmeric, cumin, and coriander.\n3. Add peas and paneer and cook through.\n4. Simmer until the sauce thickens.\n5. Serve hot with rice.'
        ),
        Recipe(
            title='Thai Basil Chicken',
            description='Fragrant chicken stir-fry with basil and savory Thai flavors.',
            ingredients=json.dumps(['300g chicken breast', '1 cup basil leaves', '1 red chili', '2 garlic cloves', '1 tbsp soy sauce', '1 tbsp oyster sauce', '1 tsp sugar']),
            instructions='1. Sear the chicken in a hot pan.\n2. Add garlic and chili, then stir-fry briefly.\n3. Add sauces and sugar.\n4. Toss in basil leaves until wilted.\n5. Serve with rice.'
        ),
        Recipe(
            title='Vegetable Fried Rice',
            description='A satisfying, quick meal with rice, vegetables, and soy flavor.',
            ingredients=json.dumps(['2 cups cooked rice', '1 cup mixed vegetables', '2 eggs', '1 tbsp soy sauce', '1 tsp sesame oil', 'Spring onions']),
            instructions='1. Scramble the eggs in a hot pan and set aside.\n2. Stir-fry the vegetables until crisp-tender.\n3. Add rice and soy sauce and toss well.\n4. Return the eggs and spring onions.\n5. Serve immediately.'
        ),
        Recipe(
            title='Chicken Caesar Wrap',
            description='Grilled chicken in a creamy Caesar wrap with crunchy greens.',
            ingredients=json.dumps(['2 tortillas', '1 chicken breast', 'Lettuce', '1/4 cup Caesar dressing', 'Parmesan', 'Cherry tomatoes']),
            instructions='1. Grill or pan-cook the chicken until golden.\n2. Slice into strips.\n3. Layer lettuce, chicken, tomatoes, and dressing in tortillas.\n4. Add parmesan and wrap tightly.\n5. Slice and serve.'
        ),
        Recipe(
            title='Roasted Cauliflower Bowl',
            description='Crispy cauliflower served with grains, greens, and tahini drizzle.',
            ingredients=json.dumps(['1 cauliflower head', '1 cup couscous', '2 cups greens', '1 tbsp tahini', '1 tbsp lemon juice', 'Olive oil', 'Paprika']),
            instructions='1. Roast cauliflower with olive oil and paprika until golden.\n2. Prepare couscous according to package instructions.\n3. Arrange greens and couscous in bowls.\n4. Top with cauliflower and tahini-lemon drizzle.\n5. Serve warm.'
        ),
        Recipe(
            title='Beef and Broccoli Stir-Fry',
            description='Thin strips of beef tossed with broccoli in a savory glaze.',
            ingredients=json.dumps(['300g beef strips', '2 cups broccoli', '2 garlic cloves', '1 tbsp soy sauce', '1 tsp cornstarch', '1 tsp ginger', 'Sesame oil']),
            instructions='1. Marinate beef with soy sauce and cornstarch.\n2. Stir-fry beef until browned, then set aside.\n3. Cook broccoli, garlic, and ginger until crisp.\n4. Return beef and toss together.\n5. Serve with rice.'
        ),
        Recipe(
            title='Sweet Potato Chickpea Hash',
            description='A hearty skillet hash with roasted sweet potato and warm spice.',
            ingredients=json.dumps(['2 sweet potatoes', '1 cup chickpeas', '1 red onion', '1 tsp paprika', '1/2 tsp cumin', '1 tbsp olive oil', 'Parsley']),
            instructions='1. Roast or sauté sweet potato cubes until golden.\n2. Add chickpeas, onion, paprika, and cumin.\n3. Cook until everything is heated through.\n4. Finish with parsley and serve.'
        ),
        Recipe(
            title='Avocado Mango Salad',
            description='Fresh, creamy, and bright with tropical fruit and greens.',
            ingredients=json.dumps(['1 mango', '1 avocado', '2 cups mixed greens', '1/2 cup cucumber', '1 tbsp lime juice', 'Salt', 'Pepper']),
            instructions='1. Cut mango and avocado into bite-size pieces.\n2. Toss with greens and cucumber.\n3. Drizzle with lime juice and season lightly.\n4. Serve immediately.'
        ),
        Recipe(
            title='Chicken Alfredo Pasta',
            description='Creamy, rich pasta with tender chicken and parmesan.',
            ingredients=json.dumps(['200g pasta', '1 chicken breast', '1/2 cup cream', '1/4 cup parmesan', '2 garlic cloves', 'Butter', 'Parsley']),
            instructions='1. Cook pasta until al dente.\n2. Sauté chicken until cooked through and slice it.\n3. Make a quick garlic butter cream sauce.\n4. Add pasta and chicken, tossing to coat.\n5. Finish with parmesan and parsley.'
        ),
        Recipe(
            title='Stuffed Bell Peppers',
            description='Bell peppers loaded with rice, herbs, and cheese.',
            ingredients=json.dumps(['4 bell peppers', '1 cup cooked rice', '1/2 cup black beans', '1/2 cup corn', '1/2 cup cheese', '1 tbsp herbs', 'Tomato sauce']),
            instructions='1. Halve the peppers and remove seeds.\n2. Mix rice, beans, corn, cheese, and herbs.\n3. Fill the peppers and top with a little tomato sauce.\n4. Bake until tender and golden.'
        ),
        Recipe(
            title='Lemon Herb Fish',
            description='Flaky fish fillets with a zesty lemon-herb glaze.',
            ingredients=json.dumps(['2 fish fillets', '1 lemon', '1 tbsp butter', '1 tbsp parsley', '1 tsp oregano', 'Salt', 'Pepper']),
            instructions='1. Season fish with salt, pepper, and oregano.\n2. Sear in butter and lemon juice.\n3. Add parsley and cook until flakes separate.\n4. Serve with vegetables or rice.'
        ),
        Recipe(
            title='Classic Ratatouille',
            description='A rustic vegetable stew bursting with flavor and color.',
            ingredients=json.dumps(['1 zucchini', '1 eggplant', '2 tomatoes', '1 onion', '2 garlic cloves', 'Olive oil', 'Herbs']),
            instructions='1. Sauté onion and garlic until soft.\n2. Add chopped vegetables and cook slowly.\n3. Season with herbs and olive oil.\n4. Simmer until the vegetables break down and become rich.'
        ),
        Recipe(
            title='Tomato Basil Risotto',
            description='Creamy arborio rice with ripe tomatoes and fresh basil.',
            ingredients=json.dumps(['1 cup arborio rice', '2 cups vegetable stock', '1 cup tomato puree', '1/4 cup parmesan', '1 tbsp butter', 'Fresh basil']),
            instructions='1. Sauté rice lightly in butter.\n2. Add stock gradually while stirring.\n3. Fold in tomato puree and cook until creamy.\n4. Finish with parmesan and basil.\n5. Serve warm.'
        ),
        Recipe(
            title='Mediterranean Chicken Traybake',
            description='Roasted chicken with peppers, olives, and lemon.',
            ingredients=json.dumps(['2 chicken thighs', '1 red pepper', '1 yellow pepper', '10 olives', '1 lemon', '1 tbsp olive oil', 'Oregano']),
            instructions='1. Toss the vegetables with olive oil and oregano.\n2. Roast chicken and vegetables together until golden.\n3. Add olives in the last 10 minutes.\n4. Serve with lemon wedges.'
        ),
        Recipe(
            title='Pesto Pasta Salad',
            description='Cool pasta tossed with pesto, peas, and cherry tomatoes.',
            ingredients=json.dumps(['200g pasta', '1/2 cup peas', '1/2 cup cherry tomatoes', '2 tbsp pesto', '1/4 cup mozzarella', 'Leafy greens']),
            instructions='1. Cook the pasta and cool it slightly.\n2. Mix with peas, tomatoes, greens, and pesto.\n3. Add mozzarella for extra richness.\n4. Chill or serve immediately.'
        ),
        Recipe(
            title='Turkey Meatballs',
            description='Juicy turkey meatballs in a simple tomato sauce.',
            ingredients=json.dumps(['500g ground turkey', '1 egg', '1/4 cup breadcrumbs', '1 cup tomato sauce', '1 tsp garlic powder', 'Parmesan']),
            instructions='1. Mix turkey with egg, breadcrumbs, and seasoning.\n2. Shape into meatballs and bake until cooked.\n3. Simmer in tomato sauce until glossy.\n4. Finish with parmesan and serve.'
        ),
        Recipe(
            title='Butternut Squash Soup',
            description='A silky autumn soup with roasted squash and warm spices.',
            ingredients=json.dumps(['2 cups roasted squash', '1 onion', '2 cups vegetable stock', '1/2 cup cream', '1/2 tsp nutmeg', 'Pepper', 'Salt']),
            instructions='1. Sauté onion until soft.\n2. Add squash and stock, then simmer gently.\n3. Blend until smooth.\n4. Stir in cream and nutmeg.\n5. Serve topped with pepper and salt.'
        ),
        Recipe(
            title='Honey Garlic Chicken Thighs',
            description='Sticky, savory chicken thighs glazed with honey and garlic.',
            ingredients=json.dumps(['4 chicken thighs', '2 tbsp honey', '2 garlic cloves', '1 tbsp soy sauce', '1 tbsp butter', 'Salt', 'Pepper']),
            instructions='1. Season chicken and sear until browned.\n2. Add garlic, honey, and soy sauce.\n3. Simmer until the glaze thickens.\n4. Finish with butter and serve.'
        ),
        Recipe(
            title='Palak Dal',
            description='Yellow lentils cooked with spinach in a comforting Indian style.',
            ingredients=json.dumps(['1 cup yellow lentils', '2 cups spinach', '1 onion', '1 tomato', '1 tsp cumin', '1/2 tsp turmeric', 'Salt']),
            instructions='1. Cook lentils until tender.\n2. Sauté onion, tomato, cumin, and turmeric.\n3. Add spinach and cook until wilted.\n4. Mix with cooked lentils and simmer.\n5. Season and serve with rice.'
        ),
        Recipe(
            title='Mexican Black Bean Tacos',
            description='Quick tacos packed with beans, corn, and fresh toppings.',
            ingredients=json.dumps(['6 tortillas', '1 cup black beans', '1/2 cup corn', '1/2 avocado', 'Lime', 'Cabbage', 'Chili powder']),
            instructions='1. Warm the tortillas.\n2. Sauté black beans with chili powder.\n3. Fill tacos with beans, corn, cabbage, and avocado.\n4. Squeeze lime over the top and serve.'
        ),
        Recipe(
            title='Pork Chops with Apples',
            description='Savory pork chops paired with sautéed apples and thyme.',
            ingredients=json.dumps(['2 pork chops', '2 apples', '1 tbsp butter', '1 tsp thyme', 'Salt', 'Pepper', 'Olive oil']),
            instructions='1. Season pork chops and sear until golden.\n2. Cook sliced apples in butter with thyme.\n3. Serve pork chops with apples on the side.\n4. Add a fresh salad if desired.'
        )
    ]

    db.session.add_all(sample_recipes)
    db.session.commit()


with app.app_context():
    db.create_all()
    seed_recipes()

# Routes
@app.route('/')
def index():
    # Fetch all recipes, newest first
    recipes = Recipe.query.order_by(Recipe.date_created.desc()).all()
    return render_template('index.html', recipes=recipes)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        # Get all dynamic ingredient inputs as a list
        ingredients_list = request.form.getlist('ingredient[]')
        # Clean up empty inputs and convert to JSON string
        ingredients = json.dumps([i.strip() for i in ingredients_list if i.strip()])
        instructions = request.form.get('instructions')
        
        new_recipe = Recipe(title=title, description=description, ingredients=ingredients, instructions=instructions)
        db.session.add(new_recipe)
        db.session.commit()
        
        flash('Recipe added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_edit.html', action='Add', recipe=None)

@app.route('/recipe/<int:id>')
def view_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    # Convert JSON string back to Python list
    ingredients = json.loads(recipe.ingredients)
    return render_template('recipe.html', recipe=recipe, ingredients=ingredients)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    if request.method == 'POST':
        recipe.title = request.form.get('title')
        recipe.description = request.form.get('description')
        ingredients_list = request.form.getlist('ingredient[]')
        recipe.ingredients = json.dumps([i.strip() for i in ingredients_list if i.strip()])
        recipe.instructions = request.form.get('instructions')
        
        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('view_recipe', id=recipe.id))
    
    ingredients = json.loads(recipe.ingredients)
    return render_template('add_edit.html', action='Edit', recipe=recipe, ingredients=ingredients)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_recipes()
    app.run(debug=True)
