import { createStore } from 'vuex' 
const store = createStore({ 
    state: {
        authenticated: false,
        token: ''
    }, 
    getters: {},
    mutations: {
        SET_AUTH(state, payload) {
            state.authenticated = payload
        },
        set_token(state, payload) {
            state.token = payload
        }
    },
    actions: {
        setAuth(context, payload) {
            context.commit('SET_AUTH', payload)
        },
        setToken(context, payload) {
            context.commit('set_token', payload)
        } 
    }, 
})

export default store;