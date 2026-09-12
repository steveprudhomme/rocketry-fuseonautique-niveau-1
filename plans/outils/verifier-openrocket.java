// 2026-09-12 — contrôle reproductible OpenRocket 24.12, JDK 21.
// Ne modifie pas les fichiers. Les avertissements de vol sont affichés,
// pas supprimés; ils ne sont pas des erreurs de lecture XML.
import java.io.File;
import info.openrocket.core.startup.OpenRocketCore;
import info.openrocket.core.file.GeneralRocketLoader;
import info.openrocket.core.masscalc.MassCalculator;

class VerifierOpenRocket {
    public static void main(String[] args) throws Exception {
        if (args.length == 0) throw new IllegalArgumentException("Indiquer les fichiers .xml ou .ork");
        System.setProperty("java.awt.headless", "true");
        System.setProperty("openrocket.bypass.presets", "true");
        OpenRocketCore.initialize();
        for (String path : args) {
            var loader = new GeneralRocketLoader(new File(path));
            var doc = loader.load();
            if (!loader.getWarnings().isEmpty())
                throw new IllegalStateException("Import: " + loader.getWarnings());
            var stage = doc.getRocket().getStage(0);
            double length = 0;
            for (var c : stage.getChildren()) length += c.getLength();
            if (Math.abs(length - 1.1938) > 1e-8)
                throw new IllegalStateException("Longueur exposee attendue: 1.1938 m; obtenue: " + length);
            if (doc.getSimulations().size() != 4)
                throw new IllegalStateException("Quatre simulations attendues");
            // Régression v1.1 : profil LOC à cinq sommets, pas un trapèze.
            info.openrocket.core.rocketcomponent.FinSet fin = null;
            for (var c : stage.getChild(2).getChildren())
                if (c instanceof info.openrocket.core.rocketcomponent.FinSet f) fin = f;
            if (!(fin instanceof info.openrocket.core.rocketcomponent.FreeformFinSet))
                throw new IllegalStateException("Profil libre LOC attendu");
            double[][] expected = {{0,0},{.142875,.10795},{.206375,.10795},{.206375,.03175},{.17145,0}};
            var points = fin.getFinPoints();
            if (points.length != expected.length) throw new IllegalStateException("Cinq sommets attendus");
            for (int i=0; i<points.length; i++)
                if (Math.abs(points[i].x-expected[i][0])>1e-8 || Math.abs(points[i].y-expected[i][1])>1e-8)
                    throw new IllegalStateException("Sommet LOC incorrect: " + i);
            if (Math.abs(fin.getAxialOffset()-.41275)>1e-8 || Math.abs(fin.getTabLength()-.117475)>1e-8
                || Math.abs(fin.getTabHeight()-.029972)>1e-8 || Math.abs(fin.getTabOffset()-.0381)>1e-8)
                throw new IllegalStateException("Position ou languette LOC incorrecte");
            var dry = MassCalculator.calculateStructure(doc.getRocket().getSelectedConfiguration());
            System.out.println("OK import " + path + "; masse estimee sans moteur (kg)="
                + dry.getMass() + "; CG depuis pointe (m)=" + dry.getCM().x);
            for (var sim : doc.getSimulations()) {
                sim.simulate();
                var data = sim.getSimulatedData();
                if (!Double.isFinite(data.getMaxAltitude()) || data.getMaxAltitude() <= 0)
                    throw new IllegalStateException("Vol invalide: " + sim.getName());
                System.out.println("OK simulation " + sim.getName() + "; apogee (m)="
                    + data.getMaxAltitude() + "; avertissements=" + data.getWarningSet());
            }
        }
        System.exit(0);
    }
}
