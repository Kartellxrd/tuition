import React,{useEffect,useState}from"react";
import{ActivityIndicator,Pressable,StyleSheet,Text,View}from"react-native";
import Ionicons from"@expo/vector-icons/Ionicons";
import Screen from"../../components/Screen";
import{Muted,Title}from"../../components/UI";
import{api}from"../../api/client";
import{colors}from"../../theme";

export default function ModulesScreen({navigation}){
 const[modules,setModules]=useState([]),[loading,setLoading]=useState(true);
 useEffect(()=>{api.get("/modules").then(r=>setModules(r.data)).finally(()=>setLoading(false))},[]);
 return <Screen>
  <Text style={s.eyebrow}>YOUR LEARNING</Text>
  <Title>Choose a module</Title>
  <Muted>Start with the subject. Inside, choose Group Tuition, One-on-One, Reading Week Revision or Supplementary Prep.</Muted>
  <View style={s.spacer}/>
  {loading?<ActivityIndicator color={colors.cyan}/>:modules.map((m,i)=>
   <Pressable key={m.id} onPress={()=>navigation.navigate("ModuleOptions",{module:m})} style={({pressed})=>[s.card,pressed&&{opacity:.8}]}>
    <View style={s.row}>
     <View style={s.icon}><Ionicons name={i%2?"hardware-chip-outline":"code-slash"} size={24} color={colors.cyan}/></View>
     <View style={s.flex}>
      <Text style={s.code}>{m.code}</Text>
      <Text style={s.name}>{m.name}</Text>
     </View>
     <Ionicons name="arrow-forward" size={22} color={colors.cyan}/>
    </View>
    {!!m.description&&<Text style={s.desc} numberOfLines={3}>{m.description}</Text>}
    <View style={s.tags}><Text style={s.tag}>GROUP</Text><Text style={s.tag}>1-ON-1</Text><Text style={s.tag}>EXAM SUPPORT</Text></View>
   </Pressable>)}
 </Screen>
}
const s=StyleSheet.create({
 eyebrow:{color:colors.cyan,fontWeight:"900",fontSize:12,letterSpacing:1.6,marginBottom:8},
 spacer:{height:16},card:{backgroundColor:colors.card,borderWidth:1,borderColor:"#1D3150",borderRadius:22,padding:18,marginBottom:16},
 row:{flexDirection:"row",alignItems:"center",gap:13},flex:{flex:1},icon:{width:48,height:48,borderRadius:15,backgroundColor:"#09243A",alignItems:"center",justifyContent:"center"},
 code:{color:colors.cyan,fontWeight:"900",fontSize:13,letterSpacing:1},name:{color:colors.white,fontWeight:"900",fontSize:19,marginTop:3},
 desc:{color:colors.muted,lineHeight:20,marginTop:14},tags:{flexDirection:"row",flexWrap:"wrap",gap:7,marginTop:16},
 tag:{color:"#BAE6FD",backgroundColor:"#10243B",paddingHorizontal:9,paddingVertical:6,borderRadius:9,fontSize:10,fontWeight:"800"}
});