function getCard() {
    
    try {
        TPDirect.card.getPrime(function (result) {
            console.log(result);
            if (result.status !== 0) {
                console.error('getPrime 错误:', result.msg);
                alert('获取 Prime 失败，请检查卡片信息或网络连接。');
                return;
            }
            let prime = result.card.prime;
            
            console.log('获取 Prime 成功: ' + prime);
            orders(prime);
        });
    } catch (error) {
        console.error('getPrime 函数调用错误:', error);
        alert('获取 Prime 时发生错误，请稍后重试或联系客服。');
    }
   
}
function orders(prime){
    let token = localStorage.getItem("authToken");
    console.log("order",prime);

    fetch("/api/orders",{
        method:"POST",
        headers:{
            "Content-Type": "application/json",
            "Authorization": `${token}`
        },
        body:JSON.stringify({"prime":prime})
    }).then((res)=>console.log("OK"))
}