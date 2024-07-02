function getPrime(bookData,user_id) {
    try {
        TPDirect.card.getPrime(function (result) {
            console.log(result);
            if (result.status !== 0) {
                console.error("getPrime Error:", result.msg);
                return;
            }
            let prime = result.card.prime;
            // console.log("Get Prime Successed: " + prime);
            bookData["prime"] = prime;
            orders(bookData,user_id);
        });
    } catch (error) {
        console.error("Get prime failed, try again later", error);
        alert("Get prime failed, try again later");
    }
}

async function orders(bookData,user_id) {
    let token = localStorage.getItem("authToken");
    if (!token) {
        console.error("Authorization token is missing.");
        alert("Authorization token is missing.");
        return;
    }

    try {
        document.getElementById("loading").style.display = "flex";
        let res = await fetch("/api/orders", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `${token}`
            },
            body: JSON.stringify(bookData)
        });

        let result = await res.json();
        if (!res.ok) {
            throw new Error(result.message);
        }
        console.log(result);
        let order_status = result["data"]["payment"]["status"];
        attraction_id = bookData["order"]["trip"]["attraction"]["id"];
        if (order_status === 0){
            let del_result = await deleteSchedule(user_id,attraction_id);
        }
        window.location.href = `/thankyou?number=${result["data"]["number"]}`;

        } catch (err) {
            console.error(err);
            alert(err);
        }finally{
            document.getElementById("loading").style.display = "none";
        }
}
