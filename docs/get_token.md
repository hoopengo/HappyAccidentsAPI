# How to get token?

1. Go to <https://www.happyaccidents.ai/>
2. Sign in
3. Open console (F12)
4. Write this script:

 ```js
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}
JSON.parse(decodeURIComponent(getCookie("supabase-auth-token")))[0]
```

5. Save token
