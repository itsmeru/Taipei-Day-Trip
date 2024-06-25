async function renderBook(result,tokenData){
    let bookSection = document.querySelector(".book-section");
    let formDisplay = document.querySelectorAll(".form-section,.book-section,hr");
    let priceDisplay = document.querySelector(".total-price");
    let firstHr = document.querySelector(".hrFirst");
    let footDown = document.querySelector(".down");
    
    let user_id = tokenData["id"];
    let userName = tokenData["name"];
    let email = tokenData["email"];
    let bookTitle = document.querySelector(".book-title");
    bookTitle.textContent = `您好，${userName}，待預定的行程如下：`;
    if (result === null){
        let noneDiv = document.createElement("div");
        noneDiv.className = "body font-medium none-book";
        noneDiv.textContent = "目前沒有任何待預定行程";
        bookTitle.parentNode.insertBefore(noneDiv, bookTitle.nextSibling);
        priceDisplay.style.display = "none";
        footDown.style.flex = 1;

        formDisplay.forEach((element) => {
            if (element.tagName === "HR") {
                element.style.display = "none";
            } else {
              element.style.display = result ? "block" : "none";
            }
          });
        firstHr.style.display = "block";
        return;
    }
    firstHr.style.display = "block";
    let data = result["data"];
    let attraction_id = data["attractions"]["id"];
    let images = data["attractions"]["images"];
    let address = data["attractions"]["address"];
    let attractionName = data["attractions"]["name"];
    let date = data["date"];
    let price = `新台幣 ${data["price"]} 元`;
    let time = data["time"]=="morning"?"早上9點到下午4點":"下午2點到晚上9點";

   

    let bookImage = document.createElement("div");
    bookImage.className = "book-image";
    let book_img = document.createElement("img");
    book_img.setAttribute("src", images);
    bookImage.appendChild(book_img);
    bookSection.appendChild(bookImage);


    let bookInfo = document.createElement("div");
    bookInfo.className = "book-info";
    
    let bookDiv = document.createElement("div");
    bookDiv.className = "title-delete";
    let titletext = document.createElement("div");
    titletext.className = "body font-bold title-text";
    titletext.textContent = `台北一日遊：${attractionName}`
    let delImage = document.createElement("div");
    delImage.className = "del-image";
    let del_img = document.createElement("img");
    del_img.setAttribute("src", "/static/pic/delete.png");
    del_img.onclick = function(){deleteSchedule(user_id,attraction_id);}
    delImage.appendChild(del_img);
    bookDiv.append(titletext,delImage);

    bookInfo.appendChild(bookDiv);



    let title = ["日期","時間","費用","地點"];
    let info = [date,time,price,address];
    for(let i= 0;i<4;i++){
        let Div = document.createElement("div");
        Div.className = "info-container"
        let Title = document.createElement("div");
        Title.className = "body font-bold";
        Title.textContent = `${title[i]} : `
        let Text = document.createElement("div");
        Text.className = "body font-medium";
        Text.textContent = `${info[i]}`;
        Div.append(Title,Text);
        bookInfo.appendChild(Div);
    }
    bookSection.appendChild(bookInfo);

    
    let nameInput = document.getElementById("nameInput");
    let emailInput = document.getElementById("emailInput");
    nameInput.value = userName;
    emailInput.value = email;
        
    let totalPrice = document.querySelector(".total-price");
    let priceText = document.createElement("div");
    priceText.className = "body font-bold price-text";
    priceText.textContent = `總價：${price}`;
    let priceBtn = document.createElement("button");
    priceBtn.className = "btn font-regular price-btn";
    priceBtn.textContent = "確認訂購並付款";
    totalPrice.append(priceText,priceBtn);

    
}
