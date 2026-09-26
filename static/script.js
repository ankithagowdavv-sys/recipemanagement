document.addEventListener("DOMContentLoaded", () => {
    
    // 1. Search Functionality (Filters recipes on the index page)
    const searchBar = document.getElementById('searchBar');
    if (searchBar) {
        searchBar.addEventListener('keyup', function(e) {
            const query = e.target.value.toLowerCase();
            const recipeCards = document.querySelectorAll('.recipe-card-container');
            
            recipeCards.forEach(card => {
                const title = card.querySelector('.recipe-title').textContent.toLowerCase();
                const desc = card.querySelector('.recipe-desc').textContent.toLowerCase();
                
                if (title.includes(query) || desc.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // 2. Dynamic Ingredient Inputs (For Add/Edit pages)
    const addIngredientBtn = document.getElementById('addIngredientBtn');
    const ingredientList = document.getElementById('ingredientList');

    if (addIngredientBtn && ingredientList) {
        addIngredientBtn.addEventListener('click', () => {
            // Create new row
            const newRow = document.createElement('div');
            newRow.className = 'input-group mb-2 ingredient-row';
            
            // Add HTML structure
            newRow.innerHTML = `
                <input type="text" name="ingredient[]" class="form-control" placeholder="New ingredient" required>
                <button type="button" class="btn btn-outline-danger remove-btn">X</button>
            `;
            
            ingredientList.appendChild(newRow);
        });

        // Event delegation for removing ingredients
        ingredientList.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-btn')) {
                // Ensure at least one ingredient field remains
                if (document.querySelectorAll('.ingredient-row').length > 1) {
                    e.target.closest('.ingredient-row').remove();
                } else {
                    alert("A recipe needs at least one ingredient!");
                }
            }
        });
    }
});
