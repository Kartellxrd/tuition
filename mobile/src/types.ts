export type Role="STUDENT"|"TUTOR";export type EnrollmentStatus="PENDING"|"ACTIVE"|"REJECTED";export type Tier="GROUP"|"ONE_ON_ONE";
export type User={id:string;name:string;email:string;role:Role;email_verified:boolean;active:boolean};
export type Module={id:string;code:string;name:string;description?:string;group_price:string;one_on_one_price:string;active:boolean};
