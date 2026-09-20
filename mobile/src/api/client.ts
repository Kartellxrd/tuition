import axios from "axios";import * as Keychain from "react-native-keychain";
export const api=axios.create({baseURL:"http://10.0.2.2:8000/api/v1",timeout:15000});
api.interceptors.request.use(async config=>{const c=await Keychain.getGenericPassword();if(c) config.headers.Authorization=`Bearer ${c.password}`;return config;});
api.interceptors.response.use(r=>r,async e=>{if(e.response?.status===401) await Keychain.resetGenericPassword();return Promise.reject(e);});
export async function saveToken(token:string){await Keychain.setGenericPassword("access_token",token)}
export async function clearToken(){await Keychain.resetGenericPassword()}
