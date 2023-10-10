addProductToCart = async (product_id) => {
    buy = document.getElementById(`buy-${product_id}`)
    cart = document.getElementById(`buy-cart-${product_id}`)
    resp = await makeRequestAddProductToCart(product_id, 1)
    buy.className = "buy-button-hidden buy-button"
    cart.className = "buy-button-cart buy-button"
};

deleteProductFromCart = async (product_id) => {
    buy = document.getElementById(`buy-${product_id}`)
    cart = document.getElementById(`buy-cart-${product_id}`)
    resp = await makeRequestAddProductToCart(product_id, 0)
    buy.className = "buy-button"
    cart.className = "buy-button-hidden buy-button-cart buy-button"
}

