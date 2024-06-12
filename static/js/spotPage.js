async function spotPage(id){
    // let res = await fetch(`/api/attraction/${id}`);
    // let datas = await res.json();
    fetch(`/api/attraction/${id}`)
    .then(res=>{
        if(!res.ok){
            throw new Error("Response was not ok");
        }
        return res.json();
        
    }).then(datas=>{
        let data = datas["data"];
        renderInfo(data["address"],data["category"],data["description"],data["MRT"],data["name"],data["transpot"],data["images"]);
    }).catch(err=>{
        console.log(err.message);
        window.location.href="/";
    })
    
}