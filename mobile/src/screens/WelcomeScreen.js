import React,{useEffect,useRef}from"react";
import{Animated,SafeAreaView,ScrollView,StyleSheet,Text,TouchableOpacity,View}from"react-native";
import{colors}from"../theme";

const modules=[
 {code:"CSI141",title:"Programming Principles",copy:"Build your problem-solving and coding confidence."},
 {code:"CSI161",title:"Introduction to Computing",copy:"Understand computing fundamentals with simple explanations."}
];
const benefits=["Clear explanations + practical examples","Past questions + exam preparation","One-on-one + group sessions","Friendly, supportive tutoring"];

export default function WelcomeScreen({navigation}){
 const fade=useRef(new Animated.Value(0)).current;
 const rise=useRef(new Animated.Value(28)).current;
 const pulse=useRef(new Animated.Value(.35)).current;
 useEffect(()=>{
  Animated.parallel([
   Animated.timing(fade,{toValue:1,duration:650,useNativeDriver:true}),
   Animated.spring(rise,{toValue:0,tension:45,friction:8,useNativeDriver:true})
  ]).start();
  Animated.loop(Animated.sequence([
   Animated.timing(pulse,{toValue:1,duration:1400,useNativeDriver:true}),
   Animated.timing(pulse,{toValue:.35,duration:1400,useNativeDriver:true})
  ])).start();
 },[]);
 return <SafeAreaView style={s.page}>
  <Animated.View pointerEvents="none" style={[s.glow,{opacity:pulse}]}/>
  <ScrollView contentContainerStyle={s.content} showsVerticalScrollIndicator={false}>
   <Animated.View style={{opacity:fade,transform:[{translateY:rise}]}}>
    <View style={s.topRow}><View><Text style={s.brand}>CODE READY</Text><Text style={s.tutors}>T U T O R S</Text></View><View style={s.live}><View style={s.dot}/><Text style={s.liveText}>FIRST-YEAR FOCUSED</Text></View></View>
    <Text style={s.eyebrow}>YOUR FIRST STEP TO A STRONGER SEMESTER</Text>
    <Text style={s.heroWhite}>MASTER CODE.</Text><Text style={s.heroCyan}>BUILD FUTURES.</Text><Text style={s.heroWhite}>BE READY.</Text>
    <Text style={s.copy}>Expert tutoring for first-year students to help you <Text style={s.accent}>learn, code and succeed.</Text></Text>
    <TouchableOpacity activeOpacity={.86} style={s.primary} onPress={()=>navigation.navigate("Register")}><View><Text style={s.primaryTitle}>GET STARTED  →</Text><Text style={s.primarySub}>Create your student account</Text></View></TouchableOpacity>
    <TouchableOpacity activeOpacity={.8} style={s.secondary} onPress={()=>navigation.navigate("Login")}><Text style={s.secondaryTitle}>SIGN IN</Text><Text style={s.secondarySub}>Already have an account?</Text></TouchableOpacity>
   </Animated.View>

   <View style={s.section}><Text style={s.kicker}>OUR MODULES</Text><Text style={s.sectionTitle}>FOCUS. LEARN. EXCEL.</Text>
    {modules.map(m=><View key={m.code} style={s.card}><View style={s.codeBox}><Text style={s.code}>{m.code}</Text></View><View style={s.cardBody}><Text style={s.cardTitle}>{m.title}</Text><Text style={s.cardCopy}>{m.copy}</Text></View></View>)}
   </View>

   <View style={s.section}><Text style={s.kicker}>WHY CODE READY?</Text>
    <View style={s.grid}>{benefits.map((b,i)=><View key={b} style={s.benefit}><Text style={s.benefitIcon}>{["⌁","✓","◎","♡"][i]}</Text><Text style={s.benefitText}>{b}</Text></View>)}</View>
   </View>

   <View style={s.price}><View><Text style={s.priceLabel}>AFFORDABLE RATES</Text><Text style={s.priceCopy}>Quality tutoring that fits your budget.</Text></View><View><Text style={s.amount}>P150</Text><Text style={s.per}>PER MODULE</Text></View></View>

   <View style={s.final}><Text style={s.finalWhite}>LET'S CODE YOUR</Text><Text style={s.finalCyan}>SUCCESS STORY.</Text><Text style={s.finalCopy}>Start strong. Stay ahead. Your first year is your foundation — let's build it together.</Text><TouchableOpacity style={s.finalButton} onPress={()=>navigation.navigate("Register")}><Text style={s.finalButtonText}>JOIN CODE READY  →</Text></TouchableOpacity></View>
   <Text style={s.footer}>FIRST-YEAR FOCUSED  •  BETTER UNDERSTANDING  •  BETTER RESULTS</Text>
  </ScrollView>
 </SafeAreaView>
}
const s=StyleSheet.create({
 page:{flex:1,backgroundColor:"#020817"},content:{padding:22,paddingBottom:42},glow:{position:"absolute",top:-80,right:-90,width:250,height:250,borderRadius:125,backgroundColor:"#00D9FF"},
 topRow:{flexDirection:"row",justifyContent:"space-between",alignItems:"center",marginTop:12,marginBottom:42},brand:{color:"#F8FAFC",fontSize:22,fontWeight:"900",letterSpacing:1.5},tutors:{color:"#22D3EE",fontSize:11,fontWeight:"800",letterSpacing:5,textAlign:"center"},live:{flexDirection:"row",alignItems:"center",borderWidth:1,borderColor:"#164E63",paddingHorizontal:9,paddingVertical:6,borderRadius:20},dot:{width:6,height:6,borderRadius:3,backgroundColor:"#22D3EE",marginRight:6},liveText:{fontSize:8,color:"#A5F3FC",fontWeight:"800",letterSpacing:1},
 eyebrow:{color:"#94A3B8",fontSize:10,fontWeight:"700",letterSpacing:2.2,marginBottom:12},heroWhite:{color:"#F8FAFC",fontSize:43,lineHeight:46,fontWeight:"900"},heroCyan:{color:"#22D3EE",fontSize:43,lineHeight:46,fontWeight:"900"},copy:{color:"#CBD5E1",fontSize:16,lineHeight:24,marginTop:20,marginBottom:24,maxWidth:520},accent:{color:"#22D3EE",fontWeight:"800"},
 primary:{backgroundColor:"#22D3EE",borderRadius:18,padding:19,marginBottom:12},primaryTitle:{color:"#03111F",fontSize:19,fontWeight:"900"},primarySub:{color:"#083344",fontSize:13,marginTop:2},secondary:{borderWidth:1,borderColor:"#22D3EE",borderRadius:18,padding:18,marginBottom:10},secondaryTitle:{color:"#F8FAFC",fontSize:17,fontWeight:"900"},secondarySub:{color:"#94A3B8",fontSize:13,marginTop:2},
 section:{marginTop:42},kicker:{color:"#22D3EE",fontSize:10,fontWeight:"900",letterSpacing:2.6,marginBottom:8},sectionTitle:{color:"#F8FAFC",fontSize:27,fontWeight:"900",marginBottom:17},card:{flexDirection:"row",alignItems:"center",borderWidth:1,borderColor:"#164E63",backgroundColor:"#061426",borderRadius:18,padding:15,marginBottom:12},codeBox:{borderWidth:1,borderColor:"#0891B2",borderRadius:13,paddingVertical:16,paddingHorizontal:10,marginRight:14},code:{color:"#22D3EE",fontWeight:"900",fontSize:16},cardBody:{flex:1},cardTitle:{color:"#F8FAFC",fontSize:17,fontWeight:"800"},cardCopy:{color:"#94A3B8",fontSize:13,lineHeight:19,marginTop:4},
 grid:{flexDirection:"row",flexWrap:"wrap",justifyContent:"space-between"},benefit:{width:"48%",minHeight:120,borderWidth:1,borderColor:"#123A52",backgroundColor:"#061426",borderRadius:17,padding:14,marginBottom:12},benefitIcon:{color:"#22D3EE",fontSize:28,fontWeight:"700"},benefitText:{color:"#E2E8F0",fontSize:13,lineHeight:18,marginTop:8},
 price:{marginTop:32,borderWidth:1,borderColor:"#22D3EE",borderRadius:20,padding:20,flexDirection:"row",justifyContent:"space-between",alignItems:"center",backgroundColor:"#061426"},priceLabel:{color:"#F8FAFC",fontWeight:"900",fontSize:15},priceCopy:{color:"#67E8F9",fontSize:11,marginTop:4,maxWidth:150},amount:{color:"#22D3EE",fontSize:34,fontWeight:"900",textAlign:"right"},per:{color:"#F8FAFC",fontSize:12,fontWeight:"800",textAlign:"right"},
 final:{marginTop:42},finalWhite:{color:"#F8FAFC",fontSize:28,fontWeight:"900"},finalCyan:{color:"#22D3EE",fontSize:31,fontWeight:"900"},finalCopy:{color:"#94A3B8",fontSize:14,lineHeight:21,marginVertical:15},finalButton:{backgroundColor:"#0E7490",borderRadius:15,padding:16,alignItems:"center"},finalButtonText:{color:"#ECFEFF",fontWeight:"900",letterSpacing:.5},footer:{color:"#64748B",fontSize:9,textAlign:"center",letterSpacing:1.2,marginTop:34}
});