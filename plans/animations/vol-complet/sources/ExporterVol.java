import java.io.*;
import java.util.*;
import info.openrocket.core.startup.OpenRocketCore;
import info.openrocket.core.file.GeneralRocketLoader;
import info.openrocket.core.simulation.FlightDataType;
class ExporterVol {
 public static void main(String[] args) throws Exception {
  System.setProperty("java.awt.headless","true");
  System.setProperty("openrocket.bypass.presets","true");
  OpenRocketCore.initialize();
  var loader=new GeneralRocketLoader(new File(args[0])); var doc=loader.load();
  if(!loader.getWarnings().isEmpty()) throw new Exception(loader.getWarnings().toString());
  var sim=doc.getSimulations().stream().filter(s->s.getName().contains("H143") && s.getName().toLowerCase().contains("apog")).findFirst().orElseThrow();
  sim.simulate();var data=sim.getSimulatedData();var b=data.getBranch(0);
  var types=new FlightDataType[]{FlightDataType.TYPE_TIME,FlightDataType.TYPE_POSITION_X,FlightDataType.TYPE_POSITION_Y,FlightDataType.TYPE_ALTITUDE,FlightDataType.TYPE_VELOCITY_Z,FlightDataType.TYPE_VELOCITY_TOTAL,FlightDataType.TYPE_THRUST_FORCE};
  try(var out=new PrintWriter(args[1],"UTF-8")) {
   out.println("time_s,x_m,y_m,altitude_m,vz_m_s,speed_m_s,thrust_N");
   for(int i=0;i<b.get(FlightDataType.TYPE_TIME).size();i++){for(int j=0;j<types.length;j++){if(j>0)out.print(",");out.print(b.get(types[j]).get(i));}out.println();}
  }
  try(var out=new PrintWriter(args[2],"UTF-8")){out.println("event,time_s");for(var e:b.getEvents())out.println(e.getType().name()+","+e.getTime());}
  System.out.println("EXPORTED "+sim.getName()+"; apogee="+data.getMaxAltitude()+"; warnings="+data.getWarningSet());System.exit(0);
 }
}
