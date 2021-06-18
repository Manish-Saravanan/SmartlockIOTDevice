import asyncio
import requests
from time import sleep
from filelock import Filelock

def signUp(email, password):
    response = requests.post(
            "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyBKSxqtkMKDs3zHlbrerPj5azaAQcV1sms",
            data = {
                "email": email,
                "password": password
                }
            )
    print(response)
    print(response.json())
    with open("token.txt", "w") as tokenFile:
        tokenFile.write(response.json()["idToken"])
    with open("refreshToken.txt", "w") as refreshTokenFile:
        refreshTokenFile.write(response.json()["refreshToken"])

async def getToken():
    while True:
        expiryTime = 120
        sleep(expiryTime - 5)
        with open("refreshToken.txt", "rw+") as refreshTokenFile:
            refreshToken = refreshTokenFile.read()
            response = requests.post(
                    "https://securetoken.googleapis.com/v1/token?key=AIzaSyBKSxqtkMKDs3zHlbrerPj5azaAQcV1sms",
                    data = {
                        "grant_type": "refresh_token",
                        "refresh_token": refreshToken
                        }
                    )
            refreshTokenFile.write(response.json()["refreshToken"])
        with Filelock("token.txt"):
            with open("token.txt", "w") as tokenFile:
                tokenFile.write(response.json()["idToken"])
        expiryTime = response.json()["expiresIn"]

def signIn(email, password):
    response = requests.post(
            "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyBKSxqtkMKDs3zHlbrerPj5azaAQcV1sms",
            data = {
                "email": email,
                "password": password,
                "returnSecureToken": True
                }
            )
    with open("token.txt", "w") as tokenFile:
        tokenFile.write(response.json()["idToken"])
    with open("refreshToken.txt", "w") as refreshTokenFile:
        refreshTokenFile.write(response.json()["refreshToken"])

signUp("tpmsomrolc.manishs12c@gmail.com", "Helloworld")
signIn("tpmsomrolc.manishs12c@gmail.com", "Helloworld")

asyncio.run(getToken())


