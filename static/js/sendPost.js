let token = localStorage.getItem("authToken");

async function sendPost(){
    let text = document.getElementById("textInput").value;
    let picture = document.getElementById("pictureInput").files[0];

    if (!text || !picture){
        alert("內容不得為空");
        return ;
    }
    document.getElementById("uploadStatus").style.display = "block";

    let formData = new FormData();
    formData.append("text", text);
    formData.append("picture", picture);
    let response = await fetch("/api/upload", {
        method: "POST",
        headers:{
        "Authorization": `${token}`,
        },
        body: formData
    });
    
    let result = await response.json();
    
    if (result.success) {
        document.getElementById("uploadStatus").style.display = "none";
        window.location.reload();

    } else {
        document.getElementById("uploadStatus").style.display = "none";
        alert("上傳失敗，請重試。");
    }
}
async function showPost(){
    let res = await fetch("/api/showPost",{
        method :"GET",
        headers:{
            "Content-Type":"application/json",
            "Authorization": `${token}`
        }
    })
    let results = await res.json();
    let postContainer = document.querySelector(".postContainer");
    if(res.ok){
        results.forEach(result => {
            if(result.text === null){
                console.log("OK");
                let container = document.createElement("div");
                container.className = "container";

                let postElement = document.createElement("div");
                postElement.className = "post-text";
                postElement.textContent = "尚未有新貼文";
                container.appendChild(postElement);
                postContainer.appendChild(container);
            }
            else{
                let container = document.createElement("div");
                container.className = "container";
    
                let postElement = document.createElement("div");
                postElement.className = "post-text";
                postElement.textContent = result.text;
    
                let imageElement = new Image();
                imageElement.className = "post-img";
                imageElement.src = result.imageUrl;
    
                container.appendChild(postElement);
                container.appendChild(imageElement);
                postContainer.appendChild(container);
            }
           
           
        });
    }
}