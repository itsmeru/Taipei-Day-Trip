async function searchOrder() {
    let orderNumber = document.getElementById("order_num").value;
    if (orderNumber === ""){
        alert("請輸入查詢單號");
        return;
    }
    window.location.href = `/thankyou?number=${orderNumber}`;
}

async function renderOrder(){
    let queryString = window.location.search;
    let urlParams = new URLSearchParams(queryString);
    let orderNumber = urlParams.get("number");
    if (orderNumber){
        result = await search(orderNumber);
        if (result.data === null){
            alert("查無此行程，請再次確認訂單號碼");
            window.location.href="/thankyou";
            return;
        }
        document.querySelector(".form-container").style.display = "none";
        document.querySelector(".result-container").style.display = "block";
        document.querySelector("body").style.backgroundImage = "url('/static/pic/fin.jpg')";
      
        let orderNum = result.data.number;
        let spot = result.data.trip.attraction.name;
        let address = result.data.trip.attraction.address;
        let date = result.data.trip.date;
        let time = result.data.trip.time;
        let contactNmae = result.data.contact.name;
        let contactPhone = result.data.contact.phone;
        let orderStatus = result.data.status;
        let url = result.data.trip.attraction.image;
        let title = ["訂單編號","訂購景點","地址","日期","時間","聯絡人","電話"];
        let content = [orderNum,spot,address,date,time,contactNmae,contactPhone];
        let orderInfo = document.querySelector(".order-info");
        let orderPic = document.querySelector(".order-pic");
        for(let i = 0;i<8;i++){
            let div = document.createElement("div");
            
            if(i===7 && orderStatus === 1){
                div.textContent = "付款已完成，請記下訂單編號以供確認";
                div.className = "status-sucess";
            }
            else if (i===7 && orderStatus === 0){
                div.textContent = "付款尚未完成，按此立刻前往付款";
                div.className = "status-fail";
                div.onclick = function(){window.location.href="/booking"};
            }
            else{
                div.className = "body font-medium"
                div.textContent = `${title[i]}: ${content[i]}`;
            }
            orderInfo.appendChild(div);
        }
        let img = new Image();
        img.src = url;
        orderPic.appendChild(img);
       
    }
    
}

async function search(orderNumber){
    let token = localStorage.getItem("authToken");
    if (token === null){
        alert("請重新登入");
        return;
    }
    try {
        let res = await fetch(`/api/order/${orderNumber}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `${token}`,
            },
        });
        let result = await res.json();
        
        return result;
    } catch (error) {
        console.error("Error fetching order:", error);
    }
}
