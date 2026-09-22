import React,{useState}from"react";
import{Pressable,StyleSheet,TextInput,View}from"react-native";
import Ionicons from"@expo/vector-icons/Ionicons";
import{colors}from"../theme";

export default function PasswordInput(props){
 const[visible,setVisible]=useState(false);
 return <View style={s.wrap}>
  <TextInput {...props} placeholderTextColor={colors.muted} secureTextEntry={!visible} style={s.input}/>
  <Pressable accessibilityRole="button" accessibilityLabel={visible?"Hide password":"Show password"} onPress={()=>setVisible(v=>!v)} style={s.eye}>
   <Ionicons name={visible?"eye-off-outline":"eye-outline"} size={22} color={colors.muted}/>
  </Pressable>
 </View>
}
const s=StyleSheet.create({
 wrap:{backgroundColor:colors.card,borderRadius:14,borderWidth:1,borderColor:"#24324C",marginTop:12,flexDirection:"row",alignItems:"center"},
 input:{flex:1,color:colors.white,paddingLeft:16,paddingRight:8,paddingVertical:14},
 eye:{paddingHorizontal:14,paddingVertical:12}
});