function addToCart(id, name, price) {
    fetch('/api/carts', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(data => data.json()).then(data => {
        let carts = document.getElementsByClassName('cart-counter');
        for (let c of carts)
            c.innerText = data.total_quantity;
    });
}

function updateCart(productId, obj) {
    fetch(`/api/carts/${productId}`, {
        method: 'patch',
        body: JSON.stringify({
            'quantity': obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(data => data.json()).then(data => {
        let carts = document.getElementsByClassName('cart-counter');
        for (let c of carts)
            c.innerText = data.total_quantity;

        let cartAmounts = document.getElementsByClassName('cart-amount');
        for (let c of cartAmounts)
            c.innerText = data.total_amount.toLocaleString('en');
    });
}

function deleteCart(productId) {
    if (confirm("Bạn chắc chắn xóa không?") == true) {
        fetch(`/api/carts/${productId}`, {
            method: 'delete'
        }).then(data => data.json()).then(data => {
            let carts = document.getElementsByClassName('cart-counter');
            for (let c of carts)
                c.innerText = data.total_quantity;

            let cartAmounts = document.getElementsByClassName('cart-amount');
            for (let c of cartAmounts)
                c.innerText = data.total_amount.toLocaleString('en');

            let e = document.getElementById(`cart${productId}`);
            e.style.display = 'none';
        });
    }


}

function pay() {
    if (confirm("Bạn chắc chắn thanh toán?") == true) {
        fetch('/api/pay', {
            'method': 'post'
        }).then(res => {
            if (res.status === 200)
                location.reload();
            else
                alert("Hệ thống đang có lỗi, vui lòng quay lại sau!");
        })
    }
}