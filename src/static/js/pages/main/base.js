BASE_URL = "http://127.0.0.1:8000/"

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

makeRequestAddProductToCart = async (product_id, quantity) => {
    const response = await fetch(BASE_URL + "shop/cart-update/", {
        headers: { 'X-CSRFToken': getCookie("csrftoken") },
        method: "PUT",
        body: JSON.stringify({ "product_id": product_id, "quantity": quantity }),
        credentials: 'same-origin'
    })
    return await response.json()
}