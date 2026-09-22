import React,{useCallback,useState}from"react";
import{ActivityIndicator,Pressable,StyleSheet,Text,View}from"react-native";
import Ionicons from"@expo/vector-icons/Ionicons";
import{useFocusEffect}from"@react-navigation/native";
import Screen from"../../components/Screen";
import{Muted,Title}from"../../components/UI";
import{api}from"../../api/client";
import{colors}from"../../theme";

const label=t=>(t||"").replaceAll("_"," ");
export default function LearningScreen({navigation}){
 const[items,setItems]=useState([]),[sessions,setSessions]=useState([]),[tasks,setTasks]=useState([]),[loading,setLoading]=useState(true);
 const load=useCallback(()=>{setLoading(true);Promise.all([api.get("/enrollments/me"),api.get("/sessions/me/upcoming"),api.get("/quizzes/me/todo")]).then(([e,s,t])=>{setItems(e.data);setSessions(s.data);setTasks(t.data)}).catch(()=>{}).finally(()=>setLoading(false))},[]);
 useFocusEffect(useCallback(()=>{load()},[load]));
 const active=items.filter(x=>x.status==="ACTIVE"),pending=items.filter(x=>x.status==="PENDING");
 const nextFor=e=>sessions.find(s=>s.module_id===e.module_id&&(s.enrollment_id==null||s.enrollment_id===e.id));
 return <Screen>
  <Text style={s.eyebrow}>YOUR LEARNING JOURNEY</Text><Title>My Learning</Title><Muted>Your enrolled modules, classes and learning spaces in one place.</Muted>
  {loading?<ActivityIndicator style={{marginTop:28}} color={colors.cyan}/>:<>
   <View style={s.summary}><View><Text style={s.count}>{active.length}</Text><Text style={s.summaryText}>Active</Text></View><View style={s.divider}/><View><Text style={s.count}>{pending.length}</Text><Text style={s.summaryText}>Pending</Text></View></View>
   <Text style={s.section}>TO DO</Text>
   {tasks.length===0?<View style={s.todoEmpty}><Ionicons name="checkmark-circle-outline" size={20} color={colors.success}/><Text style={s.todoEmptyText}>You're all caught up.</Text></View>:tasks.slice(0,4).map(t=><Pressable key={t.id} onPress={()=>navigation.navigate("TakeQuiz",{quizId:t.id})} style={s.todo}>
    <View style={s.todoIcon}><Ionicons name="document-text-outline" size={21} color={colors.cyan}/></View><View style={s.flex}><Text style={s.todoType}>QUIZ · {t.module_code}</Text><Text style={s.todoTitle}>{t.title}</Text><Text style={s.todoHint}>Ready to complete</Text></View><Ionicons name="chevron-forward" size={19} color={colors.cyan}/>
   </Pressable>)}
   <Text style={s.section}>ACTIVE LEARNING</Text>
   {active.length===0?<View style={s.empty}><Ionicons name="book-outline" size={27} color={colors.cyan}/><Text style={s.emptyTitle}>No active learning yet</Text><Muted>Your approved enrollments will appear here.</Muted></View>:active.map(e=>{const next=nextFor(e);return <Pressable key={e.id} onPress={()=>navigation.navigate("ModuleHub",{enrollment:e})} style={({pressed})=>[s.card,pressed&&{opacity:.82}]}>
    <View style={s.top}><View style={s.moduleIcon}><Ionicons name="code-slash" size={23} color={colors.cyan}/></View><View style={s.flex}><Text style={s.code}>{e.module_code||"MODULE"}</Text><Text style={s.name}>{e.module_name||"Your module"}</Text></View><View style={s.activePill}><Text style={s.activeText}>ACTIVE</Text></View></View>
    <View style={s.tierRow}><Ionicons name={e.tier==="ONE_ON_ONE"?"person-outline":"people-outline"} size={17} color={colors.muted}/><Text style={s.tier}>{label(e.tier)}</Text></View>
    <View style={s.next}><Ionicons name="calendar-outline" size={21} color={colors.cyan}/><View style={s.flex}><Text style={s.nextLabel}>NEXT CLASS</Text><Text style={s.nextText}>{next?new Date(next.start_at).toLocaleString():"No upcoming class scheduled"}</Text>{next?.location?<Text style={s.location}>{next.location}</Text>:null}</View><Ionicons name="chevron-forward" size={20} color={colors.cyan}/></View>
    <Text style={s.open}>OPEN LEARNING SPACE →</Text>
   </Pressable>})}
   {pending.length>0&&<><Text style={s.section}>PENDING ENROLLMENTS</Text>{pending.map(e=><View key={e.id} style={s.pending}><View style={s.flex}><Text style={s.pendingCode}>{e.module_code||"MODULE"} · {label(e.tier)}</Text><Text style={s.pendingText}>Payment verification pending</Text></View><Ionicons name="time-outline" size={22} color="#FBBF24"/></View>)}</>}
  </>}
 </Screen>
}
const s=StyleSheet.create({
 eyebrow:{color:colors.cyan,fontSize:11,fontWeight:"900",letterSpacing:1.5,marginBottom:8},summary:{flexDirection:"row",alignItems:"center",backgroundColor:"#0B1426",borderRadius:18,borderWidth:1,borderColor:"#17243B",padding:16,marginTop:20,gap:22},
 count:{color:colors.white,fontSize:24,fontWeight:"900"},summaryText:{color:colors.muted,fontSize:12},divider:{height:34,width:1,backgroundColor:"#24324C"},section:{color:colors.muted,fontSize:11,fontWeight:"900",letterSpacing:1.5,marginTop:27,marginBottom:9},
 card:{backgroundColor:colors.card,borderWidth:1,borderColor:"#21627A",borderRadius:22,padding:17,marginBottom:15},top:{flexDirection:"row",alignItems:"center",gap:11},moduleIcon:{width:44,height:44,borderRadius:14,backgroundColor:"#09243A",alignItems:"center",justifyContent:"center"},flex:{flex:1},
 code:{color:colors.white,fontSize:20,fontWeight:"900"},name:{color:colors.muted,fontSize:13,marginTop:2},activePill:{backgroundColor:"#123E32",paddingHorizontal:9,paddingVertical:6,borderRadius:20},activeText:{color:"#86EFAC",fontSize:10,fontWeight:"900"},
 tierRow:{flexDirection:"row",gap:7,alignItems:"center",marginTop:15},tier:{color:"#CBD5E1",fontWeight:"800",fontSize:12},next:{flexDirection:"row",alignItems:"center",gap:11,backgroundColor:"#0A1324",borderRadius:15,padding:13,marginTop:14},
 nextLabel:{color:colors.cyan,fontSize:9,fontWeight:"900",letterSpacing:1},nextText:{color:colors.white,fontWeight:"800",fontSize:13,marginTop:3},location:{color:colors.muted,fontSize:11,marginTop:3},open:{color:colors.cyan,fontSize:11,fontWeight:"900",marginTop:15},
 empty:{backgroundColor:colors.card,borderRadius:18,padding:20,borderWidth:1,borderColor:"#1D3150"},emptyTitle:{color:colors.white,fontWeight:"900",fontSize:17,marginTop:10,marginBottom:4},
 todo:{flexDirection:"row",alignItems:"center",gap:11,backgroundColor:"#0B1426",borderWidth:1,borderColor:"#1D3150",borderRadius:16,padding:14,marginBottom:9},todoIcon:{width:40,height:40,borderRadius:12,backgroundColor:"#10243B",alignItems:"center",justifyContent:"center"},todoType:{color:colors.cyan,fontSize:9,fontWeight:"900",letterSpacing:1},todoTitle:{color:colors.white,fontWeight:"900",fontSize:15,marginTop:3},todoHint:{color:colors.muted,fontSize:11,marginTop:3},todoEmpty:{flexDirection:"row",alignItems:"center",gap:9,backgroundColor:"#0B1426",borderRadius:15,padding:14},todoEmptyText:{color:"#CBD5E1",fontWeight:"700"},pending:{flexDirection:"row",alignItems:"center",backgroundColor:"#111827",borderRadius:17,borderWidth:1,borderColor:"#3A3440",padding:16,marginBottom:10},pendingCode:{color:colors.white,fontWeight:"900"},pendingText:{color:"#FBBF24",fontSize:12,marginTop:5}
});