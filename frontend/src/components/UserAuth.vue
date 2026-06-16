<template>
    <div class="Container">
        <h1 class="text-center">Welcome to Chatified!</h1>
        <div id="auth-container" class="row">
            <div class="col-sm-4 offset-sm-4">
                <ul class="nav nav-tabs nav-justified" id="myTab" role="tablist">
                    <li class="nav-item">
                        <a class="nav-link activate" id="signup-tab" data-toggle="tab"
                        href="#signup" role="tab" aria-controls="signup" aria-selected="true">Sign Up</a>
                    </li>

                    <li class="nav-item">
                        <a class="nav-link activate" id="signin-tab" data-toggle="tab"
                        href="#signin" role="tab" aria-controls="signin" aria-selected="false">Sign In</a>
                    </li>
                </ul>

                <div class="tab-content" id="myTabContent">
                    <div class="tab-pane fade show active" id="signup"
                    role="tabpanel" aria-labelledby="signin-tab">
                        <form @submit.prevent="signUp">
                            <div class="form-group">
                                <input v-model="email" type="email" class="form-control"
                                id="email" placeholder="Email Address" required>
                            </div>
                            <div class="form-row">
                                <div class="form-group col-md-6">
                                    <input v-model="username" type="username" class="form-control"
                                    id="username" placeholder="Username" required>
                                </div>
                                <div class="form-group col-md-6">
                                    <input v-model="password" type="password" class="form-control"
                                    id="password" placeholder="Password" required>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox"
                                    id="toc" required>
                                    <label class="form-check-label" for="gridCheck">
                                        Accept terms and Conditions
                                    </label>
                                </div>
                            </div>
                            <button type="submit" class="btn btn-block btn-primary">Sign Up</button>
                        </form>
                    </div>
                </div>

                <div class="tab-pane fade" id="signin" role="tabpanel"
                aria-labelledby="signin-tab">
                    <form @submit.prevent="signIn">
                        <div class="form-group">
                            <input v-model="username" type="text" class="form-control"
                            id="signin-username" placeholder="Username" required>
                        </div>
                        <div class="form-group">
                            <input v-model="password" type="password" class="form-control"
                            id="signin-password" placeholder="Password" required>
                        </div>

                        <button type="submit" class="btn btn-black btn-primary">Sign In</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
function postJson (url, data) {
  return new Promise((resolve, reject) => {
    const request = new XMLHttpRequest()

    request.open('POST', url)
    request.setRequestHeader('Content-Type', 'application/json')

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

function setStoredValue (key, value) {
  if (window.sessionStorage) {
    window.sessionStorage.setItem(key, value)
  }
}

export default {
  data () {
    return {
      email: '',
      username: '',
      password: ''
    }
  },

  methods: {
    signUp () {
      postJson('http://localhost:8000/auth/users/', this.$data)
        .then(() => {
          alert('Your account has been created. You will be signed in automatically')
          this.signIn()
        })
        .catch((error) => {
          alert(error.message)
        })
    },

    signIn () {
      const credentials = {
        username: this.username,
        password: this.password
      }

      postJson('http://localhost:8000/auth/token/login/', credentials)
        .then((data) => {
          setStoredValue('authToken', data.auth_token)
          setStoredValue('username', this.username)
          this.$router.push('/chats')
        })
        .catch((error) => {
          alert(error.message)
        })
    }
  }
}

</script>

<style scoped>
    #auth-container {
        margin-top: 50px;
    }

    .tab-content {
        padding-top: 20px;
    }
</style>
