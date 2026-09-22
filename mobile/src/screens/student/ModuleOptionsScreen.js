import React,{useEffect,useState}from"react";
import{ActivityIndicator,Pressable,StyleSheet,Text,View}from"react-native";
import Ionicons from"@expo/vector-icons/Ionicons";
import Screen from"../../components/Screen";
import{Muted}from"../../components/UI";
import{api}from"../../api/client";
import{colors}from"../../theme";

const fallback=[
 {kind:"GROUP_TUITION",service_name:"Group Tuition",price:150,billing_period:"MODULE",sessions_per_week:3,session_minutes:60,description:"Learn consistently with other students."},
 {kind:"ONE_ON_ONE",service_name:"One-on-One",price:200,billing_period:"MODULE",description:"Personal support built around your needs."},
 {kind:"READING_WEEK",service_name:"Reading Week Revision",price:100,billing_period:"WEEK",description:"Dedicated exam revision during reading week."},
 {kind:"SUPPLEMENTARY",service_name:"Supplementary Exam Prep",price:250,billing_period:"MODULE",description:"Dedicated preparation for supplementary examinations."}
];
const meta={
 GROUP_TUITION:{icon:"people-outline",badge:"SEMESTER",lines:["3 sessions every week","1 hour per session","Revision support before assessments"]},
 ONE_ON_ONE:{icon:"person-outline",badge:"PERSONAL",lines:["Individual attention","Focus on your weak areas","Personalized pace and support"]},
 READING_WEEK:{icon:"library-outline",badge:"EXAM SEASON",lines:["Reading week only","Focused exam preparation","Open to revision-only students"]},
 SUPPLEMENTARY:{icon:"school-outline",badge:"SUPP SUPPORT",lines:["Dedicated supplementary preparation","Support outside normal semester tuition"]}
};
export default function ModuleOptionsScreen({route,navigation}){
 const m=route.params.module,[items,setItems]=useState([]),[loading,setLoading]=useState(true);
 useEffect(()=>{api.get("/offerings/module/"+m.id).then(r=>setItems(r.data)).catch(()=>setItems(fallback)).finally(()=>setLoading(false))},[m.id]);
 const semester=items.filter(x=>["GROUP_TUITION","ONE_ON_ONE"].includes(x.kind)),exam=items.filter(x=>["READING_WEEK","SUPPLEMENTARY"].includes(x.kind));
 const card=o=>{const x=meta[o.kind]||meta.GROUP_TUITION;return <Pressable key={o.id||o.kind} onPress={()=>navigation.navigate("Enroll",{module:m,offering:o})} style={({pressed})=>[s.card,o.kind==="ONE_ON_ONE"&&s.premium,pressed&&{opacity:.82}]}>
  <View style={s.top}><View style={s.icon}><Ionicons name={x.icon} size={23} color={colors.cyan}/></View><View style={s.flex}><Text style={s.badge}>{x.badge}</Text><Text style={s.name}>{o.service_name}</Text></View><Ionicons name="chevron-forward" size={21} color={colors.cyan}/></View>
  <Text style={s.desc}>{o.description}</Text>
  <View style={s.features}>{x.lines.map(v=><View key={v} style={s.feature}><Ionicons name="checkmark-circle" size={17} color={colors.success}/><Text style={s.featureText}>{v}</Text></View>)}</View>
  <View style={s.priceRow}><Text style={s.price}>P{o.price}</Text><Text style={s.period}>{o.billing_period==="WEEK"?"/ reading week":o.kind==="GROUP_TUITION"?"/ module":""}</Text><Text style={s.explore}>EXPLORE →</Text></View>
 </Pressable>};
 return <Screen>
  <Pressable onPress={()=>navigation.goBack()} style={s.back}><Ionicons name="arrow-back" size={20} color={colors.white}/><Text style={s.backText}>Modules</Text></Pressable>
  <Text style={s.code}>{m.code}</Text><Text style={s.title}>{m.name}</Text><Muted>Choose the support that fits how you want to learn.</Muted>
  {loading?<ActivityIndicator style={{marginTop:30}} color={colors.cyan}/>:<><Text style={s.section}>REGULAR TUITION</Text>{semester.map(card)}<Text style={s.section}>EXAM SUPPORT</Text>{exam.map(card)}</>}
 </Screen>
}
const s=StyleSheet.create({
 back:{flexDirection:"row",alignItems:"center",gap:8,marginBottom:24},backText:{color:colors.white,fontWeight:"800"},code:{color:colors.cyan,fontWeight:"900",fontSize:13,letterSpacing:1.5},
 title:{color:colors.white,fontSize:29,fontWeight:"900",marginTop:5,marginBottom:8},section:{color:colors.muted,fontSize:11,fontWeight:"900",letterSpacing:1.6,marginTop:28,marginBottom:8},
 card:{backgroundColor:colors.card,borderRadius:22,borderWidth:1,borderColor:"#1D3150",padding:18,marginBottom:14},premium:{borderColor:colors.cyan,borderWidth:1.5},
 top:{flexDirection:"row",alignItems:"center",gap:12},icon:{width:45,height:45,borderRadius:14,backgroundColor:"#09243A",alignItems:"center",justifyContent:"center"},flex:{flex:1},
 badge:{color:colors.cyan,fontSize:10,fontWeight:"900",letterSpacing:1},name:{color:colors.white,fontSize:19,fontWeight:"900",marginTop:3},desc:{color:colors.muted,lineHeight:20,marginTop:13},
 features:{gap:8,marginTop:14},feature:{flexDirection:"row",alignItems:"center",gap:8},featureText:{color:"#CBD5E1",fontSize:13},
 priceRow:{flexDirection:"row",alignItems:"baseline",marginTop:18,paddingTop:14,borderTopWidth:1,borderTopColor:"#1E293B"},price:{color:colors.white,fontSize:24,fontWeight:"900"},period:{color:colors.muted,fontSize:12,marginLeft:4},explore:{color:colors.cyan,fontSize:11,fontWeight:"900",marginLeft:"auto"}
});