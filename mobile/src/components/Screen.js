import React from "react";
import {KeyboardAvoidingView,Platform,SafeAreaView,ScrollView,StyleSheet,View,useWindowDimensions} from "react-native";
import {colors} from "../theme";

export default function Screen({children,scroll=true,centered=false}){
  const {width}=useWindowDimensions();
  const horizontal=width<360?16:width<600?22:28;
  const contentStyle=[s.body,{paddingHorizontal:horizontal},centered&&s.centered];
  return (
    <SafeAreaView style={s.safe}>
      <KeyboardAvoidingView style={s.flex} behavior={Platform.OS==="ios"?"padding":undefined}>
        {scroll?
          <ScrollView
            contentContainerStyle={contentStyle}
            keyboardShouldPersistTaps="handled"
            showsVerticalScrollIndicator={false}
          >{children}</ScrollView>
          :<View style={contentStyle}>{children}</View>}
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}
const s=StyleSheet.create({
  safe:{flex:1,backgroundColor:colors.background},
  flex:{flex:1},
  body:{width:"100%",maxWidth:680,alignSelf:"center",paddingTop:24,paddingBottom:40,flexGrow:1},
  centered:{justifyContent:"center",paddingTop:32,paddingBottom:32}
});