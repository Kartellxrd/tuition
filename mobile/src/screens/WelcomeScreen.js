import React,{useEffect,useRef}from"react";
import{Animated,SafeAreaView,ScrollView,StyleSheet,Text,TouchableOpacity,View,useWindowDimensions}from"react-native";

const modules=[
 {code:"CSI141",title:"Programming Principles",tag:"CODE"},
 {code:"CSI161",title:"Introduction to Computing",tag:"COMPUTING"}
];

export default function WelcomeScreen({navigation}){
 const{width}=useWindowDimensions();const compact=width<370;
 const fade=useRef(new Animated.Value(0)).current;
 const lift=useRef(new Animated.Value(18)).current;
 const orb=useRef(new Animated.Value(0)).current;
 useEffect(()=>{
  Animated.parallel([Animated.timing(fade,{toValue:1,duration:550,useNativeDriver:true}),Animated.spring(lift,{toValue:0,tension:55,friction:9,useNativeDriver:true})]).start();
  Animated.loop(Animated.sequence([Animated.timing(orb,{toValue:1,duration:2600,useNativeDriver:true}),Animated.timing(orb,{toValue:0,duration:2600,useNativeDriver:true})])).start();
 },[]);
 const drift=orb.interpolate({inputRange:[0,1],outputRange:[0,16]});
 return <SafeAreaView style={s.page}>
  <Animated.View pointerEvents="none" style={[s.orb,{transform:[{translateY:drift}]}]}/>
  <ScrollView contentContainerStyle={[s.content,{paddingHorizontal:compact?18:22}]} showsVerticalScrollIndicator={false}>
   <View style={s.nav}>
    <View><Text style={s.logo}>CODE READY</Text><Text style={s.logoSub}>TUTORS</Text></View>
    <TouchableOpacity onPress={()=>navigation.navigate("Login")} style={s.navButton}><Text style={s.navButtonText}>Sign in</Text></TouchableOpacity>
   </View>

   <Animated.View style={[s.hero,{opacity:fade,transform:[{translateY:lift}]}]}>
    <View style={s.badge}><View style={s.badgeDot}/><Text style={s.badgeText}>BUILT FOR FIRST-YEAR STUDENTS</Text></View>
    <Text style={[s.headline,{fontSize:compact?39:45}]}>Learn code.</Text>
    <Text style={[s.headline,{fontSize:compact?39:45}]}>Think <Text style={s.cyan}>smarter.</Text></Text>
    <Text style={[s.headline,{fontSize:compact?39:45}]}>Stay ahead.</Text>
    <Text style={s.subhead}>Focused tutoring for CSI141 and CSI161 — clear explanations, practical work and exam-ready preparation.</Text>
    <View style={s.actions}>
     <TouchableOpacity activeOpacity={.86} onPress={()=>navigation.navigate("Register")} style={s.primary}><Text style={s.primaryText}>Get started</Text><Text style={s.arrow}>→</Text></TouchableOpacity>
     <TouchableOpacity activeOpacity={.8} onPress={()=>navigation.navigate("Login")} style={s.textButton}><Text style={s.textButtonText}>I already have an account</Text></TouchableOpacity>
    </View>
    <View style={s.trustRow}><Text style={s.trustStrong}>CSI141</Text><Text style={s.sep}>•</Text><Text style={s.trustStrong}>CSI161</Text><Text style={s.sep}>•</Text><Text style={s.trust}>P150 / module</Text></View>
   </Animated.View>

   <View style={s.section}>
    <Text style={s.overline}>WHAT WE TEACH</Text><Text style={s.sectionTitle}>Two modules. One clear goal.</Text><Text style={s.sectionCopy}>Build the foundation you need to understand the work, solve problems and walk into assessments prepared.</Text>
    <View style={s.moduleRow}>{modules.map(m=><View key={m.code} style={s.moduleCard}><Text style={s.moduleTag}>{m.tag}</Text><Text style={s.moduleCode}>{m.code}</Text><Text style={s.moduleTitle}>{m.title}</Text><View style={s.cardLine}/><Text style={s.moduleLink}>Explore learning →</Text></View>)}</View>
   </View>

   <View style={s.section}>
    <Text style={s.overline}>THE CODE READY METHOD</Text><Text style={s.sectionTitle}>No noise. Just progress.</Text>
    <View style={s.method}>
     <View style={s.step}><Text style={s.stepNo}>01</Text><View style={s.stepBody}><Text style={s.stepTitle}>Understand</Text><Text style={s.stepCopy}>Concepts broken down into language that actually makes sense.</Text></View></View>
     <View style={s.step}><Text style={s.stepNo}>02</Text><View style={s.stepBody}><Text style={s.stepTitle}>Practice</Text><Text style={s.stepCopy}>Work through examples, problems and past-question style exercises.</Text></View></View>
     <View style={[s.step,{borderBottomWidth:0}]}><Text style={s.stepNo}>03</Text><View style={s.stepBody}><Text style={s.stepTitle}>Perform</Text><Text style={s.stepCopy}>Build confidence for quizzes, tests and exams.</Text></View></View>
    </View>
   </View>

   <View style={s.cta}><Text style={s.ctaMini}>READY WHEN YOU ARE</Text><Text style={s.ctaTitle}>Your first year sets the foundation.</Text><Text style={s.ctaCopy}>Make it count with focused support built around your modules.</Text><TouchableOpacity onPress={()=>navigation.navigate("Register")} style={s.ctaButton}><Text style={s.ctaButtonText}>Create student account</Text><Text style={s.ctaArrow}>→</Text></TouchableOpacity></View>
   <View style={s.footer}><Text style={s.footerBrand}>CODE READY TUTORS</Text><Text style={s.footerText}>LEARN • CODE • SUCCEED</Text></View>
  </ScrollView>
 </SafeAreaView>
}
const s=StyleSheet.create({
 page:{flex:1,backgroundColor:"#030712"},content:{paddingBottom:34,maxWidth:620,width:"100%",alignSelf:"center"},orb:{position:"absolute",top:80,right:-110,width:240,height:240,borderRadius:120,backgroundColor:"#083344",opacity:.28},
 nav:{height:78,flexDirection:"row",alignItems:"center",justifyContent:"space-between"},logo:{color:"#F8FAFC",fontSize:16,fontWeight:"900",letterSpacing:1.4},logoSub:{color:"#22D3EE",fontSize:8,fontWeight:"800",letterSpacing:5},navButton:{borderWidth:1,borderColor:"#1E3A4A",borderRadius:20,paddingHorizontal:16,paddingVertical:8},navButtonText:{color:"#DFFBFF",fontSize:13,fontWeight:"700"},
 hero:{paddingTop:35,paddingBottom:52},badge:{alignSelf:"flex-start",flexDirection:"row",alignItems:"center",backgroundColor:"#071725",borderWidth:1,borderColor:"#12394A",paddingHorizontal:10,paddingVertical:7,borderRadius:20,marginBottom:22},badgeDot:{width:5,height:5,borderRadius:3,backgroundColor:"#22D3EE",marginRight:7},badgeText:{color:"#8FEAF5",fontSize:8,fontWeight:"800",letterSpacing:1.3},headline:{color:"#F8FAFC",fontWeight:"900",lineHeight:49,letterSpacing:-1.5},cyan:{color:"#22D3EE"},subhead:{color:"#94A3B8",fontSize:15,lineHeight:23,maxWidth:500,marginTop:20},actions:{alignItems:"flex-start",marginTop:25},primary:{height:48,minWidth:148,flexDirection:"row",alignItems:"center",justifyContent:"center",backgroundColor:"#22D3EE",borderRadius:13,paddingHorizontal:20},primaryText:{color:"#03131B",fontSize:14,fontWeight:"900"},arrow:{color:"#03131B",fontSize:19,marginLeft:14},textButton:{paddingVertical:14},textButtonText:{color:"#A5F3FC",fontSize:12,fontWeight:"700"},trustRow:{flexDirection:"row",alignItems:"center",flexWrap:"wrap",marginTop:13},trustStrong:{color:"#E2E8F0",fontSize:11,fontWeight:"800"},trust:{color:"#64748B",fontSize:11},sep:{color:"#164E63",marginHorizontal:8},
 section:{paddingVertical:38,borderTopWidth:1,borderTopColor:"#111C2C"},overline:{color:"#22D3EE",fontSize:9,fontWeight:"900",letterSpacing:2.1,marginBottom:9},sectionTitle:{color:"#F8FAFC",fontSize:27,lineHeight:33,fontWeight:"900",letterSpacing:-.5},sectionCopy:{color:"#718096",fontSize:13,lineHeight:20,marginTop:10,marginBottom:20},moduleRow:{gap:10},moduleCard:{backgroundColor:"#07111F",borderWidth:1,borderColor:"#132337",borderRadius:16,padding:18,marginBottom:10},moduleTag:{color:"#64748B",fontSize:8,fontWeight:"900",letterSpacing:1.5},moduleCode:{color:"#22D3EE",fontSize:23,fontWeight:"900",marginTop:13},moduleTitle:{color:"#E2E8F0",fontSize:14,fontWeight:"700",marginTop:2},cardLine:{height:1,backgroundColor:"#12263A",marginVertical:15},moduleLink:{color:"#78909C",fontSize:11,fontWeight:"600"},
 method:{marginTop:18,backgroundColor:"#07111F",borderRadius:16,borderWidth:1,borderColor:"#132337",paddingHorizontal:17},step:{flexDirection:"row",paddingVertical:18,borderBottomWidth:1,borderBottomColor:"#132337"},stepNo:{color:"#22D3EE",fontSize:10,fontWeight:"900",marginRight:16,marginTop:3},stepBody:{flex:1},stepTitle:{color:"#F1F5F9",fontSize:15,fontWeight:"800"},stepCopy:{color:"#718096",fontSize:12,lineHeight:18,marginTop:4},
 cta:{marginTop:12,backgroundColor:"#071725",borderWidth:1,borderColor:"#155E75",borderRadius:20,padding:22},ctaMini:{color:"#22D3EE",fontSize:8,fontWeight:"900",letterSpacing:2},ctaTitle:{color:"#F8FAFC",fontSize:25,lineHeight:31,fontWeight:"900",marginTop:10},ctaCopy:{color:"#8B9BAD",fontSize:13,lineHeight:20,marginTop:8},ctaButton:{alignSelf:"flex-start",height:45,flexDirection:"row",alignItems:"center",backgroundColor:"#F8FAFC",borderRadius:12,paddingHorizontal:17,marginTop:20},ctaButtonText:{color:"#06111F",fontSize:12,fontWeight:"900"},ctaArrow:{color:"#06111F",fontSize:17,marginLeft:12},
 footer:{paddingTop:32,alignItems:"center"},footerBrand:{color:"#CBD5E1",fontSize:10,fontWeight:"900",letterSpacing:1.7},footerText:{color:"#475569",fontSize:8,fontWeight:"700",letterSpacing:2,marginTop:5}
});