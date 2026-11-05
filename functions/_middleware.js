// Canonical host redirect: www -> apex (301), runs before all routes/static assets.
export async function onRequest(context) {
  const url = new URL(context.request.url);
  if (url.hostname === "www.plugreports.com") {
    url.hostname = "plugreports.com";
    return Response.redirect(url.toString(), 301);
  }
  return context.next();
}
