async function signUp(form) {
  let res = await fetch("/api/user", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: form.name.value,
      email: form.email.value,
      password: form.password.value,
    }),
  });
  let result = await res.json();
  if (!res.ok) {
    alert(result.message);
    form.reset();
  } else {
    alert("註冊成功");
    closeDialog("register-dialog");
    form.reset();
  }
}
async function signIn(form) {
  try {
    let res = await fetch("/api/user/auth", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: form.email.value,
        password: form.password.value,
      }),
    });

    if (!res.ok) {
      let err = await res.json();
      throw new Error(err.message);
    }

    let result = await res.json();
    alert("登入成功");
    localStorage.setItem("authToken", result.token);
    closeDialog("login-dialog");
    form.reset();
  } catch (err) {
    alert(err.message);
    form.reset();
  }
}
