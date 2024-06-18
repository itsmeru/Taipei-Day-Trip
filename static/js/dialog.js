function removeMessage(dialog, selector) {
  let messageDiv = dialog.querySelector(selector);
  if (messageDiv) {
    messageDiv.remove();
  }
}

function openDialog(dialogId) {
  let dialog = document.getElementById(dialogId);
  removeMessage(dialog, ".error-message");
  removeMessage(dialog, ".msg");
  dialog.showModal();
}

function closeDialog(dialogId) {
  let dialog = document.getElementById(dialogId);
  removeMessage(dialog, ".error-message");
  removeMessage(dialog, ".msg");
  dialog.close();
}

function toggleDialogs(openDialogId) {
  let dialogs = document.querySelectorAll("dialog");
  dialogs.forEach((dialog) => {
    removeMessage(dialog, ".error-message");
    removeMessage(dialog, ".msg");
    dialog.close();
  });
  openDialog(openDialogId);
}


function clearMessage(form) {
  removeMessage(form, ".error-message");
  removeMessage(form, ".msg");
}
