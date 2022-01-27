async function onLogin(user_name) {
  try {
    const credential_info = await create_assersion(user_name);
    const result = await login_user(credential_info);
    return result;
  } catch(e) {
    console.error(e);
    return e.message;
  }
}

async function create_assersion(user_name) {
  const form = document.querySelector('form');
  const data = {
    'name': user_name,
  };
  const res = await do_fetch('/webauthn/authenticate/begin', data);
  const credential_info = await navigator.credentials.get(res);
  return credential_info;
}

async function login_user(credentialInfo) {
  var assertion_data = {
    'credentialRawId': new Uint8Array(credentialInfo.rawId),
    'authenticatorData': new Uint8Array(credentialInfo.response.authenticatorData),
    'clientDataJSON': new Uint8Array(credentialInfo.response.clientDataJSON),
    'signature': new Uint8Array(credentialInfo.response.signature),
    'userHandle': new Uint8Array(credentialInfo.response.userHandle)
  };
  const res = await do_fetch('/webauthn/authenticate/complete', assertion_data);
  return res.display_name;
} 