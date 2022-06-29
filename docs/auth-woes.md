# Authentication Woes

## Goal

Create a button that authenticates a user and deploys a language (or any arbitrary) resource on behalf of them.

## Constraints

1. The website should not need hosting. I.e., it should be distributed via a zip file.
2. The authentication process should be simpler than deploying a resource using the Azure portal or the Azure CLI.

## The `client_id`

When authenticating to Azure, I need to give it a client id. I can make my own app in AAD or I could use the Developer CLI app.
To make my app work, I need to give it the contributor role to the Developer Playground subscription, but when I try to log in
using `InteractiveBrowserCredential` or `DeviceCodeCredential`, I get an administration error:

> Need admin approval
> 
> unverified
> 
> needs permission to access resources in your organization that only an admin can grant. Please ask an admin to grant permission to this app before you can use it.

This means that I have to use the Microsoft Azure CLI app, which I have much less control over.

## `InteractiveBrowserCredential`

My first attempt was to use `InteractiveBrowserCredential`, because it does exactly what I want.
In JavaScript, I pass it a `client_id` of the Azure CLI app and I have a choice of passing it a `redirectUri`. This is where
the authentication server will send the auth code. If I don't pass it anything, then it will default to the current URL. This isn't
great because the `file://` protocol is blocked. I can pass it something along the lines of `https://localhost:8400` (this is what
Python's `InteractiveBrowserCredential` does by default) and open the authorization
endpoint in a popup. This way I can (I think) extract the authentication code
from the parent window. But even with this, I get CORS error when hitting the token.~~~~
I also tried the native client backend and it just led me to a blank page.
Both authorization flow and implicit grant flow require a redirect URI [RFC 6749 section 3.1.2] and must be able to receive
incoming requests [section 4.1]

The closest idea I have to get this to work is to authenticate with a popup, have the popup redirect
to `localhost:8400`, and have the user copy and paste the auth code from
the url, or copy and paste the url and parse it in JavaScript.

Another thing I tried is making a simple Http server at `localhost:8400` authenticating from there because the token endpoint
does not support CORS.

At this point, it felt more like I was looking for security exploits than ways to create
an interactive login. The idea was as follows:

1. Use implicit grant authorization flow with a `redirectUri` of `localhost:8400`.
2. Open the `/authorize` endpoint in a popup
3. The popup would then redirect to `localhost:8400` with they key as a fragment or query param
4. It doesn't matter that there isn't anything in `localhost:8400` because I can access the id token using `popup.location.href` in the parent window.
5. Close the popup before the user sees anything suspicious
6. ta-da, I now have an id token

Unfortunately, step 4 failed also because of CORS. The browser would not let me access
data in the popup window because it had a different origin.

## `DeviceCodeCredential`

After talking to Karishma in the JavaScript team and Matt in our team, they suggested I use device code authentication, which would
eliminate the need of a redirect uri. The first warning sign was when I imported `DeviceCodeCredential` from the JavaScript SDK and
I got an error saying that `DeviceCodeCredential` could not be used in the browser.

To work around this, I tried to perform the network requests themselves. When I ran these requests in Edge, I just got
a 400 error and said that the `Content-Length` of my request was 0, but the exact same request worked in my REST client.
I tried doing the requests in Firefox and faced my worst enemy: CORS. I think the reason why device code credentials do not
work in the browser is that the `/devicecode` endpoint does not support CORS. At least it gives me an error when I
send it an `OPTIONS` request.

I can skip the preflight request by creating a `Request` object with `mode: "no-cors"`, but when I put this into fetch, it gives me
an opaque response which I cannot read from.

## B2C

Charles told me not to touch this.

## Non-OAuth2 Options

There are none:

> All of the architectures are based on the industry-standard protocols OAuth 2.0 and OpenID Connect [[Authentication flows
and application scenarios](https://docs.microsoft.com/en-us/azure/active-directory/develop/authentication-flows-app-scenarios)].
