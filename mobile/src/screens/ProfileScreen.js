import React,{useState}from"react";
import{ActivityIndicator,Image,Pressable,StyleSheet,Text,View}from"react-native";
import * as ImagePicker from"expo-image-picker";
import Ionicons from"@expo/vector-icons/Ionicons";
import Screen from"../components/Screen";
import{Button,Card,ErrorText,Muted,Title}from"../components/UI";
import PasswordInput from"../components/PasswordInput";
import{useAuth}from"../context/AuthContext";
import{api}from"../api/client";
import{colors}from"../theme";

export default function ProfileScreen(){
 const{user,logout,refreshUser}=useAuth();
 const[current,setCurrent]=useState(""),[next,setNext]=useState(""),[confirm,setConfirm]=useState("");
 const[error,setError]=useState(""),[message,setMessage]=useState(""),[busy,setBusy]=useState(false);
 const initials=(user?.name||"U").split(" ").map(x=>x[0]).slice(0,2).join("").toUpperCase();

 async function choosePhoto(){
  const permission=await ImagePicker.requestMediaLibraryPermissionsAsync();
  if(!permission.granted){setError("Photo library permission is required to choose a profile picture.");return}
  const result=await ImagePicker.launchImageLibraryAsync({mediaTypes:["images"],allowsEditing:true,aspect:[1,1],quality:.8});
  if(result.canceled)return;
  try{
   setBusy(true);setError("");setMessage("");
   const asset=result.assets[0],form=new FormData();
   form.append("file",{uri:asset.uri,name:asset.fileName||"profile.jpg",type:asset.mimeType||"image/jpeg"});
   await api.post("/auth/profile-image",form,{headers:{"Content-Type":"multipart/form-data"}});
   await refreshUser();setMessage("Profile picture updated.");
  }catch(e){setError(e.response?.data?.detail||"Could not update profile picture.")}finally{setBusy(false)}
 }
 async function changePassword(){
  setError("");setMessage("");
  if(next.length<8){setError("New password must be at least 8 characters.");return}
  if(next!==confirm){setError("New passwords do not match.");return}
  try{setBusy(true);await api.post("/auth/change-password",{current_password:current,new_password:next});setCurrent("");setNext("");setConfirm("");setMessage("Password changed successfully.")}
  catch(e){setError(e.response?.data?.detail||"Could not change password.")}finally{setBusy(false)}
 }
 return <Screen>
  <Text style={s.eyebrow}>YOUR ACCOUNT</Text><Title>Profile</Title><Muted>Manage your account, profile picture and security.</Muted>
  <View style={s.identity}>
   <Pressable onPress={choosePhoto} style={s.avatarWrap} disabled={busy}>{user?.profile_image_url?<Image source={{uri:user.profile_image_url}} style={s.avatar}/>:<View style={[s.avatar,s.fallback]}><Text style={s.initials}>{initials}</Text></View>}<View style={s.camera}><Ionicons name="camera" size={15} color="#04111D"/></View></Pressable>
   <Text style={s.name}>{user?.name}</Text><Text style={s.email}>{user?.email}</Text><View style={s.role}><Text style={s.roleText}>{user?.role}</Text></View>
   <Pressable onPress={choosePhoto} disabled={busy}><Text style={s.changePhoto}>CHANGE PROFILE PHOTO</Text></Pressable>
  </View>
  <Text style={s.section}>ACCOUNT DETAILS</Text>
  <Card><View style={s.infoRow}><Ionicons name="person-outline" size={20} color={colors.cyan}/><View><Text style={s.label}>FULL NAME</Text><Text style={s.value}>{user?.name}</Text></View></View><View style={s.rule}/><View style={s.infoRow}><Ionicons name="mail-outline" size={20} color={colors.cyan}/><View><Text style={s.label}>EMAIL</Text><Text style={s.value}>{user?.email}</Text></View></View></Card>
  <Text style={s.section}>SECURITY</Text>
  <Card><Text style={s.cardTitle}>Change password</Text><Muted>Use at least 8 characters for your new password.</Muted><PasswordInput placeholder="Current password" value={current} onChangeText={setCurrent}/><PasswordInput placeholder="New password" value={next} onChangeText={setNext}/><PasswordInput placeholder="Confirm new password" value={confirm} onChangeText={setConfirm}/><Button title={busy?"PLEASE WAIT...":"UPDATE PASSWORD"} disabled={busy||!current||!next||!confirm} onPress={changePassword}/></Card>
  <ErrorText message={error}/>{message?<Text style={s.success}>{message}</Text>:null}
  {busy?<ActivityIndicator color={colors.cyan} style={{marginVertical:10}}/>:null}
  <Button title="SIGN OUT" secondary onPress={logout}/>
 </Screen>
}
const s=StyleSheet.create({
 eyebrow:{color:colors.cyan,fontSize:11,fontWeight:"900",letterSpacing:1.5,marginBottom:8},identity:{alignItems:"center",paddingVertical:25},avatarWrap:{position:"relative"},avatar:{width:104,height:104,borderRadius:52},fallback:{backgroundColor:"#12304A",alignItems:"center",justifyContent:"center",borderWidth:2,borderColor:colors.cyan},initials:{color:colors.white,fontSize:32,fontWeight:"900"},camera:{position:"absolute",right:1,bottom:2,width:31,height:31,borderRadius:16,backgroundColor:colors.cyan,alignItems:"center",justifyContent:"center",borderWidth:3,borderColor:colors.background},name:{color:colors.white,fontSize:23,fontWeight:"900",marginTop:13},email:{color:colors.muted,fontSize:13,marginTop:4},role:{backgroundColor:"#10243B",paddingHorizontal:10,paddingVertical:5,borderRadius:20,marginTop:9},roleText:{color:"#BAE6FD",fontSize:10,fontWeight:"900"},changePhoto:{color:colors.cyan,fontSize:11,fontWeight:"900",marginTop:13},
 section:{color:colors.muted,fontSize:11,fontWeight:"900",letterSpacing:1.5,marginTop:14,marginBottom:8},infoRow:{flexDirection:"row",alignItems:"center",gap:13},label:{color:colors.muted,fontSize:9,fontWeight:"900",letterSpacing:1},value:{color:colors.white,fontWeight:"800",fontSize:14,marginTop:3},rule:{height:1,backgroundColor:"#1E293B",marginVertical:15},cardTitle:{color:colors.white,fontSize:17,fontWeight:"900",marginBottom:4},success:{color:colors.success,fontWeight:"800",marginVertical:10}
});