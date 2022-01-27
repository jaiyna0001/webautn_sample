function array_buffer_to_base64(buffer) {
  return btoa(new Uint8Array(buffer).reduce((data, byte) => data + String.fromCharCode(byte), ''));
}
function base64_to_array_buffer(data) {
  return Uint8Array.from(atob(data), c => c.charCodeAt(0)).buffer;
}
async function do_fetch(path, data) {
  const cbor_data = array_buffer_to_base64(CBOR.encode(data));
  const param = {
    method: 'POST',
    headers: {
      'Accept': 'text/plain',
      'Content-Type': 'text/plain'
    },
    body: cbor_data
  }
  const res = await fetch(path, param);
  const res_data = await res.text();
  const decode_data = CBOR.decode(base64_to_array_buffer(res_data));
  if (decode_data['status'] !== "OK") {
    throw new Error(`${path}: request error`);
  }
  return CBOR.decode(base64_to_array_buffer(res_data));
}