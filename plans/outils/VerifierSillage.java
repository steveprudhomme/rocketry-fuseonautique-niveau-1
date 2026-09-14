// Vérification avec OpenRocket 24.12 et rendu natif hors écran JOGL.
// java -cp OpenRocket-24.12.jar VerifierSillage.java fichier.ork dossier-images
import java.io.*;
import java.nio.file.*;
import java.util.*;
import javax.imageio.ImageIO;
import com.jogamp.opengl.*;
import com.jogamp.opengl.util.awt.AWTGLReadBufferUtil;
import info.openrocket.core.startup.*;
import info.openrocket.core.file.*;
import info.openrocket.core.rocketcomponent.*;
import info.openrocket.swing.gui.figure3d.*;

class VerifierSillage {
 public static void main(String[] args) throws Exception {
  System.setProperty("openrocket.bypass.presets","true");
  OpenRocketCore.initialize();
  var loader=new GeneralRocketLoader(new File(args[0]));
  var doc=loader.load();
  if(!loader.getWarnings().isEmpty())throw new IllegalStateException(loader.getWarnings().toString());
  int count=0;
  for(var comp:doc.getRocket()) {
   var a=comp.getAppearance();
   if(a!=null && a.getTexture()!=null) {
    var t=a.getTexture();
    try(var bytes=t.getImage().getBytes()) {
     var im=ImageIO.read(bytes);if(im==null)throw new IllegalStateException("Texture illisible");
     System.out.println(comp.getName()+" : "+im.getWidth()+"x"+im.getHeight()+" "+t);
    }
    count++;
   }
  }
  if(count!=2)throw new IllegalStateException("Deux textures attendues");
  System.out.println("Chargement OR sans avertissement; deux textures lues depuis archive; simulations="+doc.getSimulationCount());
  if(args.length<2){System.exit(0);}
  GLProfile profile=GLProfile.get(GLProfile.GL2);
  GLCapabilities caps=new GLCapabilities(profile);caps.setOnscreen(false);caps.setDoubleBuffered(false);
  var drawable=GLDrawableFactory.getFactory(profile).createOffscreenAutoDrawable(null,caps,null,800,1600);
  drawable.display();
  drawable.invoke(true, d->{
   try {
    var gl=d.getGL().getGL2();var rr=new RealisticRenderer(doc);rr.init(d);
    gl.glViewport(0,0,800,1600);gl.glEnable(GL.GL_DEPTH_TEST);gl.glClearDepth(1);
    gl.glMatrixMode(GL2.GL_PROJECTION);gl.glLoadIdentity();gl.glOrtho(-.36,.36,-.72,.72,-5,5);
    for(int view=0;view<2;view++) {
     gl.glClearColor(.95f,.95f,.93f,1);gl.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT);
     gl.glMatrixMode(GL2.GL_MODELVIEW);gl.glLoadIdentity();
     gl.glLightfv(GL2.GL_LIGHT1,GL2.GL_POSITION,new float[]{-2,3,4,0},0);
     // x OR va de la pointe vers l'arrière; pointe en haut dans l'image.
     gl.glRotated(-90,0,0,1);gl.glTranslated(-.6,0,0);gl.glRotated(view==0?150:-30,1,0,0);
     // Même convention main gauche et matrice texture que RocketFigure3d.setupView.
     gl.glScaled(1,1,-1);gl.glFrontFace(GL.GL_CW);
     gl.glMatrixMode(GL2.GL_TEXTURE);gl.glLoadIdentity();gl.glScaled(-1,1,1);gl.glTranslated(-1,0,0);
     gl.glMatrixMode(GL2.GL_MODELVIEW);
     rr.render(d,doc.getRocket().getSelectedConfiguration(),Collections.emptySet());
     gl.glFinish();
     var reader=new AWTGLReadBufferUtil(profile,false);
     ImageIO.write(reader.readPixelsToBufferedImage(gl,true),"png",Path.of(args[1],"apercu-openrocket-"+(view+1)+".png").toFile());
    }
    rr.dispose(d);
   }catch(Exception e){throw new RuntimeException(e);}return true;
  });
  drawable.destroy();System.out.println("Deux rendus natifs OpenRocket termines.");System.exit(0);
 }
}
