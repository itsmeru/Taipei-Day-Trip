async function spotPage(id) {
  try{
    let res = await fetch(`/api/attraction/${id}`);
    let datas = await res.json()
    let data = datas["data"];
      return data;
  }catch(err) {
    console.log(err.message);
    window.location.href = "/";
  };
  
    
}
