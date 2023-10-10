addProductToCart = async (product_id) => {
    buy = document.getElementById(`buy-${product_id}`)
    cart = document.getElementById(`buy-cart-${product_id}`)
    resp = await makeRequestAddProductToCart(product_id, 1)
    buy.className = "buy-hidden buy"
    cart.className = "buy-cart buy"
};

deleteProductFromCart = async (product_id) => {
    buy = document.getElementById(`buy-${product_id}`)
    cart = document.getElementById(`buy-cart-${product_id}`)
    resp = await makeRequestAddProductToCart(product_id, 0)
    buy.className = "buy"
    cart.className = "buy-hidden buy-cart buy"
}

