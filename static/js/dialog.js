function openDialog(dialogId) {
  document.getElementById(dialogId).showModal();
}

function closeDialog(dialogId) {
  document.getElementById(dialogId).close();
}

function toggleDialogs(openDialogId) {
  let dialogs = document.querySelectorAll("dialog");
  dialogs.forEach((dialog) => dialog.close());
  let dialog = document.getElementById(openDialogId);
  if (openDialogId === "register-dialog") {
    dialog.style.height = "332px";
  } else {
    dialog.style.height = "275px";
  }
  dialog.showModal();
}
