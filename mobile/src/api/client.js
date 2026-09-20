import axios from "axios";
import * as Keychain from "react-native-keychain";
import {API_URL} from "../config";

export const api=axios.create({baseURL:API_URL,timeout:15000});
api.interceptors.request.use(async config=>{
  const credentials=await Keychain.getGenericPassword();
  if(credentials) config.headers.Authorization=`Bearer ${credentials.password}`;
  return config;
});
export async function saveToken(token){await Keychain.setGenericPassword("access_token",token)}
export async function clearToken(){await Keychain.resetGenericPassword()}
