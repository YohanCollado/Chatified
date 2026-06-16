<template>
    <div class="container">
        <div class="row">
            <div class="col-sm-6 offset-3">
                <div v-if="sessionStarted" id="chat-container" class="cards">
                    <div
                    class="card-header text-white text-center font-weight-bold subtle subtle-blue-g">
                    Share the page URL and start chating
                    </div>

                    <div class="card-body">
                        <div class="container chat-body">
                            <div class="row chat-section">
                                <div class="col-sm-2">
                                    <img class="rounded-circle"
                                    src="http://placehold.it/40/f16000/fff&text=D"/>
                                </div>
                                <div class="col-sm-7">
                                    <span class="card-text speech-bubble speech-bubble-peer"> Hello!
                                    </span>
                                </div>
                            </div>
                            <div class="row chat-session">
                                <div class="col-sm-7 offset-3">
                                    <span class="card-text speech-bubble speech-bubble-user float-right text-white">
                                        Another chat App?
                                    </span>
                                </div>
                                <div class="sol-sm-2">
                                    <img class="rounded-circle"
                                    src="http://placehold.it/40/333333/fff&text=A"/>
                                </div>
                            </div>
                            <div class="row chat-section">
                                <div class="col-sm-2">
                                    <p class="card-text speech-bubble speech-bubble-peer">
                                        This is Chatified. Go ahead and use it!
                                        This was built using Django and Vue JS
                                    </p>
                                </div>
                            </div>
                            <div clas="row chat-section">
                                <div class="col-sm-7 offset-3">
                                    <p class="card-text speech-bubble speech-bubble-user float-right text-white">
                                        Let Me work though this thing!
                                    </p>
                                </div>
                                <div class="col-sm-2">
                                    <img class="rounded-circle"
                                    src="http://placehold.it/40/333333/fff&text=A"/>
                                </div>
                            </div>
                            <div class="row chat-section">
                                <div class="col-sm-7 offset-3">
                                    <p class="card-text speech-bubble speech-bubble-user float-right text-white">
                                        Invite People
                                    </p>
                                </div>
                                <div class="col-sm-2">
                                    <img class="rounded-circle"
                                    src="http://placehold.it/40/333333/fff&text=A"/>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer text-muted">
                        <form>
                            <div class="row">
                                <div class="col-sm-10">
                                    <input type="text" placeholder="Type a message"/>
                                </div>
                                <div class="col-sm-2">
                                    <button class="btn btn-primary">Send</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                <div v-else>
                    <h3 class="text-center"> Welcome!</h3>
                    <br/>
                    <p class="text-center">
                        To start chating just click the button below, start a new chat and invite friends
                    </p>
                    <br/>
                    <button @click="startChatSession" class="btn btn-primary btn-lg btn-block"> Start Chat</button>
                    <p v-if="errorMessage" class="text-danger chat-error">{{ errorMessage }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
function postJson (url, data, authToken) {
  return new Promise((resolve, reject) => {
    const request = new XMLHttpRequest()

    request.open('POST', url)
    request.setRequestHeader('Content-Type', 'application/json')

    if (authToken) {
      request.setRequestHeader('Authorization', `Token ${authToken}`)
    }

    request.onload = () => {
      const response = request.responseText ? JSON.parse(request.responseText) : {}

      if (request.status >= 200 && request.status < 300) {
        resolve(response)
      } else {
        reject(new Error(JSON.stringify(response)))
      }
    }

    request.onerror = () => reject(new Error('Unable to reach the server.'))
    request.send(JSON.stringify(data || {}))
  })
}

function getStoredValue (key) {
  if (!window.sessionStorage) {
    return null
  }

  return window.sessionStorage.getItem(key)
}

export default {
  data () {
    return {
      sessionStarted: false,
      errorMessage: '',
      messages: [
        {'status': 'SUCCESS',
          'uri': '040213b14a02451',
          'message': 'Hello!',
          'user': {'id': 1, 'username': 'danidee', 'email': 'osaetindaniel@gmail.com', 'first_name': '', 'last_name': ''}},

        {'status': 'SUCCESS',
          'uri': '040213b14a02451',
          'message': 'Hey whatsup! i dey',
          'user': {'id': 2, 'username': 'daniel', 'email': '', 'first_name': '', 'last_name': ''}}
      ]
    }
  },

  created () {
    this.username = getStoredValue('username')
    this.sessionStarted = Boolean(this.$route.params.uri)
  },

  methods: {
    startChatSession () {
      const authToken = getStoredValue('authToken')
      this.errorMessage = ''

      if (!authToken) {
        this.errorMessage = 'Please sign in before starting a chat.'
        this.$router.push('/auth')
        return
      }

      postJson('http://localhost:8000/api/chats/', {}, authToken)
        .then((data) => {
          this.sessionStarted = true
          this.$router.push(`/chats/${data.uri}`)
        })
        .catch((error) => {
          this.errorMessage = error.message
        })
    }
  }
}
</script>

<!-- Add scoped attribute to limit CSS to this component only-->

<style scoped>
h1,
h2 {
    font-weight: normal;
}
ul {
    list-style-type: none;
    padding: 0;
}
li {
    display: inline-block;
    margin: 0 10px;
}

.btn {
    border-radius: 0;
}

.card-footer input[type="text"]{
    background-color: #ffffff;
    color: #444444;
    padding: 7px;
    font-size: 13px;
    border: 2px solid #cccccc;
    width: 100%;
    height: 38px;
}

.card-header a {
    text-decoration: underline;
}

.card-body {
    background-color: #ddd;
}

.chat-body {
    margin-top: -15px;
    margin-bottom: -5px;
    height: 280px;
    overflow-y: auto;
}

.speech-bubble {
    display: inline-block;
    position: relative;
    border-radius: 0.4em;
    padding: 10px;
    background-color: #fff;
    font-size: 14px;
}

.subtle-blue-gradient {
    background: linear-gradient(45deg, #004bff, #007bff);
}

.speech-bubble-user::after {
    content: "";
    position: absolute;
    right: 4px;
    top: 10px;
    width: 0;
    height: 0;
    border: 20px solid transparent;
    border-left-color: #007bff;
    border-right: 0;
    border-top: 0;
    margin-top: -10px;
    margin-right: -20px;
}

.speech-bubble-peer::after {
    content: "";
    position: absolute;
    left: 3px;
    top: 10px;
    width: 0;
    height: 0;
    border: 20px solid transparent;
    border-right-color: #ffffff;
    border-top: 0;
    border-left: 0;
    margin-top: -10px;
    margin-left: -20px;
}

.chat-section:first-child {
    margin-top: 10px;
}

.chat-section {
    margin-top: 15px;
}

.send-section {
    margin-bottom: -20px;
    padding-bottom: 10px;
}

.chat-error {
    margin-top: 15px;
}
</style>
