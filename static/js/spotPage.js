async function spotPage(id){
    let res = await fetch(`/api/attraction/${id}`);
    let datas = await res.json();
    let data = datas["data"];
    renderInfo(data["address"],data["category"],data["description"],data["MRT"],data["name"],data["transpot"],data["images"]);
}