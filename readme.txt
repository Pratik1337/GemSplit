to run backend
uvicorn main:app --reload --port 8000


install ngrok, follow these steps
https://dashboard.ngrok.com/get-started/setup/macos

then in other terminal
ngrok http 8000

this will open up the ngrok and provide a random subdomain which you will have to copy and add it to the react native endpoint