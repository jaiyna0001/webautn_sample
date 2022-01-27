async function onRegist(user_name) {
  try {
    const credential_info = await create_credential(user_name);
    const result = await resiter_user(credential_info);
    return result;
  } catch(e) {
    console.error(e);
    return e.message;
  }
}

async function create_credential(user_name) {
  const form = document.querySelector('form');
  const data = {
    'name': user_name,
  };
  const res = await do_fetch('/webauthn/register/begin', data);
  const credential_info = await navigator.credentials.create(res);
  return credential_info;
}

async function resiter_user(credentialInfo) {
  const attestation_data = {
    'clientDataJSON': new Uint8Array(credentialInfo.response.clientDataJSON),
    'attestationObject': new Uint8Array(credentialInfo.response.attestationObject)
  };
  const res = await do_fetch('/webauthn/register/complete', attestation_data);
  return res.status;
}