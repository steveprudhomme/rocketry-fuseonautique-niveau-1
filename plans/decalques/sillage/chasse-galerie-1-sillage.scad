// GENERE par plans/outils/generer-sillage.py; changer la configuration, puis regenerer.
// F5 : aperçu coloré. F6/STL ne préservent pas le décor.
// Chasse Galerie 1 — projet et fusée; base technique : kit LOC-IV 4 po.
// LOC-IV 4 po — v1.1, 2026-09-12 — BROUILLON, cotes à valider sur le kit.
// Unités : mm. Origine : arrière du corps; +Z vers la pointe.
// Source principale [N] : ../notes/loc-iv-configuration-budget-niveau-1.md
// [L] https://locprecision.com/products/loc-iv (consulté 2026-09-12)
// [I] notice PK-48 liée par [L], Loc_IV_Instructions-final.pdf, p. 1-2.
// [C] https://pro38.com/wp-content/uploads/2024/11/Pro38Catalog.pdf
//     catalogue 2010 v1.0, pages PDF 15-16 (H152/H143), consulté 2026-09-12.
// [R] https://locprecision.com/products/z-clip-style-motor-retainer-set/
// [F] PK-48 Loc-IV.rkt, archive liée par [L], consultée 2026-09-12.
// SHA256 : 202acb4295f957f51e70792fe9122a7cd76edd1068706454d303ccd6a7526d8d
// Profil/position des ailerons repris de [F]; voir notes de comparaison.
// [A] = APPROXIMATION de visualisation, à mesurer avant usage dimensionnel.
// Plan d'ensemble uniquement : ni pièces de vol imprimables, ni simulation.
// Le fichier LOC_IV_4in_v0.2.scad n'a pas pu être récupéré; code reconstruit.

/* [Affichage] */
part = "assembly"; // [assembly,booster,payload,nose,coupler,bulkhead,fin,motor_mount,ring,motor,retainer,parachute,protector,cord,rail_button,prodat,eye]
view = "assembled"; // [assembled,cutaway,exploded]
recovery = "packed"; // [packed,deployed]
motor_preset = "H143"; // [H143,H152,generic_2G]
retention = "MR-1"; // [MR-1,none]
show_motor = true;
show_recovery = true;
show_protector = true;
show_rail_buttons = true;
show_prodat = false; // Accessoire au sol, jamais placé dans la fusée.
quality = 64;
explosion_gap = 180; // Décalage graphique seulement.

/* [Dimensions documentées ou nominales] */
body_d = 101.6; // [L] 4 po NOMINAL : diamètre extérieur exact à mesurer.
booster_l = 584.2; // [L,I] 23 po.
payload_l = 279.4; // [L,I] 11 po.
total_l = 1193.8; // [L] 47 po pointe/arrière du CORPS; exclut ailerons et moteur.
motor_d = 38; // [N,C] enveloppe nominale du moteur assemblé.
motor_l = 186; // [C] enveloppe moteur H143/H152; pas la cote du boîtier nu.
fin_count = 3; // [I]
fin_t = 3.175; // [L,I] 1/8 po.
ring_t = 6.35; // [L] 1/4 po.
chute_d = 914.4; // [N,L] 36 po, diamètre nominal de tissu.
cord_l = 4572; // [N,L] 15 pi; longueur stockée, tracé graphique non à longueur.
cord_w = 9.525; // [L] 3/8 po.
clip_w = 19.05; // [R] 3/4 po; reste de la géométrie [A].
mount_aft_extension = 3.175; // [I] 1/8 po derrière anneau arrière pour MR-1.
mount_front_extension = 6.35; // [I] 1/4 po devant anneau avant.

/* [Approximations à valider sur le kit reçu] */
body_wall = 1.6; // [A] 4 po nominal traité comme diamètre extérieur.
mount_id = 38.5; // [A] jeu de montage; 38 mm ne définit pas l'alésage réel.
mount_wall = 1.45; // [A]
mount_l = 300; // [A]
aft_ring_z = 6; // [A] position depuis arrière du corps.
motor_z = -5; // [A] dépassement; bague de poussée non modélisée.
// [F] Cotes du fichier de référence, PAS mesures du kit reçu.
fin_root = 171.45;
fin_span = 107.95;
fin_leading_sweep = 142.875; // Depuis bord AVANT de l'emplanture.
fin_aft_extent = 206.375; // Extrémité arrière depuis bord avant.
fin_aft_kink = 31.75; // Hauteur du sommet intermédiaire arrière.
fin_z = 0; // Racine arrière affleurant le corps : avant à 412.75 du booster.
fin_tab_length = 117.475;
fin_tab_depth = 29.972;
fin_tab_offset = 38.1; // Depuis bord AVANT de l'emplanture.
// Épaisseur fin_t : 3.175 mm [L,I] conservée; [F] indique 3 mm.
slot_clearance = 0.3; // [A] jeu purement graphique.
coupler_l = 140; // [A]
coupler_wall = 1.6; // [A]
fit_gap = 0.3; // [A] jeu diamétral.
bulkhead_t = 6.35; // [A] non déduit de l'épaisseur des anneaux.
nose_shoulder_l = 70; // [A]
nose_wall = 2; // [A] profil ellipsoïdal, pas le profil fabricant exact.
chute_pack_d = 65; // [A] volume rangé représentatif, sans étude de pliage.
chute_pack_l = 100; // [A]
protector_size = 304.8; // [A] carré de 12 po proposé, aucune taille dans [N].
fabric_t = 0.8; // [A] épaisseur graphique, non cote textile.
rail_z = [70, 430]; // [A] deux positions entre ailerons; à vérifier.
button_d = 12; // [A] « 1010 » est un type de rail, pas le diamètre du bouton.
button_neck_d = 7; // [A]
button_h = 9; // [A] visserie et perçage simplifiés.
clip_t = 1.5; // [A]
clip_reach = 20; // [A]
clip_step = 9; // [A]
eye_d = 12; // [A] œil SCM-3 et fixations schématiques.
eye_wire = 2; // [A]
prodat_d = 30; // [A] symbole cylindrique, sans fonction ni mécanisme de réglage.
prodat_l = 55; // [A]

/* [Hidden] */
$fn = quality;
eps = 0.02; // Tolérance booléenne uniquement.
fin_embed = 0.05; // Recouvrement VISUEL d'assemblage pour éviter un contact tangent
// non-manifold à la peau. La pièce fin isolée conserve le profil LOC exact.
body_id = body_d - 2*body_wall;
mount_od = mount_id + 2*mount_wall;
mount_z = aft_ring_z - mount_aft_extension;
front_ring_z = mount_z + mount_l - mount_front_extension - ring_t;
fin_tab_z = fin_z + fin_root - fin_tab_offset - fin_tab_length;
mid_ring_z = fin_tab_z + fin_tab_length + 2; // [A] juste devant languette.
coupler_d = body_id - fit_gap;
coupler_id = coupler_d - 2*coupler_wall;
nose_l = total_l - booster_l - payload_l; // DÉRIVÉ [L], 330.2 mm exposés.
gap = view == "exploded" ? explosion_gap : 0;
payload_z = booster_l + gap;
nose_z = payload_z + payload_l + gap;
pack_z = mount_z + mount_l + 45; // [A] rangement schématique.
deploy_z = nose_z + nose_l + 350; // [A] disposition explicative, pas trajectoire.

assert(quality >= 12 && body_id > mount_od && mount_id > motor_d);
assert(nose_l > 0 && body_wall > 0 && mount_wall > 0);
assert(coupler_id > 0 && nose_wall > 0 && nose_wall < body_d/2);
assert(fin_count >= 3 && fin_t > 0 && fin_span > 0);
assert(fin_leading_sweep > 0 && fin_aft_extent > fin_root && fin_aft_extent > fin_leading_sweep);
assert(fin_aft_kink > 0 && fin_aft_kink < fin_span);
assert(fin_tab_offset >= 0 && fin_tab_length > 0 && fin_tab_depth > 0);
assert(fin_tab_offset + fin_tab_length <= fin_root);
assert(aft_ring_z + ring_t < fin_tab_z && mid_ring_z + ring_t < front_ring_z,
       "Anneaux/languettes incompatibles : revoir les cotes approximatives.");
assert(front_ring_z + ring_t < booster_l - coupler_l/2);
assert(motor_z + motor_l <= mount_z + mount_l && motor_l > 0);
assert(pack_z + chute_pack_l < booster_l-coupler_l/2,
       "Volume rangé trop long pour cette représentation.");
assert(chute_pack_d < body_id && chute_pack_d > 0 && fabric_t > 0);
assert(view == "assembled" || view == "cutaway" || view == "exploded");
assert(recovery == "packed" || recovery == "deployed");
assert(motor_preset == "H143" || motor_preset == "H152" || motor_preset == "generic_2G");
assert(retention == "MR-1" || retention == "none");
parts = ["assembly","booster","payload","nose","coupler","bulkhead","fin",
         "motor_mount","ring","motor","retainer","parachute","protector",
         "cord","rail_button","prodat","eye"];
assert(len([for(p=parts) if(p == part) p]) == 1, "Nom de pièce inconnu.");
echo("BROUILLON : géométries [A] à valider; voir plans/README.md.");
echo(moteur=motor_preset, enveloppe_mm=[motor_d,motor_l], sangle_mm=cord_l);

// Primitives : tous les modules isolés sont placés à leur origine locale.
module tube(od, id, h) {
    difference() {
        cylinder(d=od,h=h);
        translate([0,0,-eps]) cylinder(d=id,h=h+2*eps);
    }
}
module shell_cut() {
    difference() {
        children();
        if(view == "cutaway") translate([-2*body_d,-2*body_d,-total_l])
            cube([4*body_d,2*body_d,4*total_l]); // Enlève y<0 des enveloppes.
    }
}
module booster() {
    difference() {
        tube(body_d,body_id,booster_l);
        for(a=[0:360/fin_count:359]) rotate([0,0,a])
            translate([mount_od/2,-(fin_t+slot_clearance)/2,fin_tab_z-eps])
                cube([body_d,fin_t+slot_clearance,fin_tab_length+2*eps]);
    }
}
module payload() { tube(body_d,body_id,payload_l); }
module coupler() { tube(coupler_d,coupler_id,coupler_l); }
module bulkhead() { cylinder(d=coupler_id,h=bulkhead_t); }
module nose() {
    // Demi-ellipsoïde creux avec épaulement ouvert; pointe arrondie approchée.
    union() {
        difference() {
            scale([body_d/2,body_d/2,nose_l]) sphere(r=1);
            scale([body_d/2-nose_wall,body_d/2-nose_wall,nose_l-nose_wall]) sphere(r=1);
            translate([-body_d,-body_d,-2*nose_l]) cube([2*body_d,2*body_d,2*nose_l]);
        }
        translate([0,0,-nose_shoulder_l])
            tube(body_id-fit_gap,body_id-fit_gap-2*nose_wall,nose_shoulder_l+eps);
    }
}
module fin() {
    // Plan local X/Z : X=0 à la peau, Z=0 à la racine arrière.
    // [F] (x avant->arrière, y radial) devient (y, fin_root-x).
    // Sommets externes : (0,0), (142.875,107.95), (206.375,107.95),
    // (206.375,31.75), (171.45,0), en coordonnées de référence LOC.
    // Languette [F] conservée : jeu radial de 0.128 mm avec le support [A].
    // Ne pas interpréter ce jeu comme une tolérance d'assemblage validée.
    rotate([90,0,0]) linear_extrude(height=fin_t,center=true)
        polygon([[0,fin_root],
                 [fin_span,fin_root-fin_leading_sweep],
                 [fin_span,fin_root-fin_aft_extent],
                 [fin_aft_kink,fin_root-fin_aft_extent],
                 [0,0],
                 [0,fin_root-fin_tab_offset-fin_tab_length],
                 [-fin_tab_depth,fin_root-fin_tab_offset-fin_tab_length],
                 [-fin_tab_depth,fin_root-fin_tab_offset],
                 [0,fin_root-fin_tab_offset]]);
}
module ring() { tube(body_id,mount_od,ring_t); }
module eye() {
    // Pas de filetage ni de rondelles; forme de repérage seulement.
    cylinder(d=eye_wire,h=8);
    translate([0,0,8+eye_d/2]) rotate([90,0,0])
        rotate_extrude() translate([eye_d/2,0]) circle(d=eye_wire);
}
module motor() {
    // Enveloppe EXTERNE uniquement. Aucun grain, tuyère, délai ou charge.
    // Les presets changent la couleur/légende, pas le volume documenté.
    color(motor_preset == "H152" ? "RoyalBlue" : "DimGray")
        cylinder(d=motor_d,h=motor_l);
}
module retainer() {
    // MR-1 = deux clips en Z + vis/écrous, PAS une bague filetée.
    // Toutes cotes sauf largeur [R] sont [A]; aucune interface validée.
    for(a=[60,240]) rotate([0,0,a]) {
        translate([motor_d/2-2,-clip_w/2,-clip_step]) {
            cube([clip_reach/2,clip_w,clip_t]);
            translate([clip_reach/2-clip_t,0,0]) cube([clip_t,clip_w,clip_step+clip_t]);
            translate([clip_reach/2-clip_t,0,clip_step]) cube([clip_reach/2+clip_t,clip_w,clip_t]);
        }
        translate([motor_d/2-2+clip_reach-3,0,0]) {
            cylinder(d=4,h=ring_t+3); // [A] vis et écrou en T sans filetage.
            translate([0,0,ring_t]) cylinder(d=9,h=2);
        }
    }
}
module rail_button() {
    difference() {
        union() {
            cylinder(d=button_d,h=button_h/3);
            cylinder(d=button_neck_d,h=button_h);
            translate([0,0,2*button_h/3]) cylinder(d=button_d,h=button_h/3);
        }
        translate([0,0,-eps]) cylinder(d=3,h=button_h+2*eps); // [A]
    }
}
module parachute() {
    if(recovery == "packed") cylinder(d=chute_pack_d,h=chute_pack_l);
    else {
        // Disque de tissu à plat : diamètre nominal, pas voile gonflée simulée.
        cylinder(d=chute_d,h=fabric_t);
        for(a=[0:45:359]) hull() { // [A] nombre/longueur des suspentes.
            // Faible résolution locale : suspentes schématiques fines.
            translate([chute_d/2*cos(a),chute_d/2*sin(a),0]) sphere(d=1.5,$fn=12);
            translate([0,0,-chute_d/2]) sphere(d=1.5,$fn=12);
        }
    }
}
module protector() {
    if(recovery == "packed")
        // Enveloppe pliée illustrative; pas une conservation de surface.
        tube(chute_pack_d+4,chute_pack_d+2,chute_pack_l);
    else translate([-protector_size/2,-protector_size/2,0])
        cube([protector_size,protector_size,fabric_t]);
}
module cord() {
    // Ruban sinusoïdal RANGÉ de repérage : ne développe pas les 4572 mm.
    for(i=[0:23]) hull() {
        translate([15*sin(i*45),0,i*4]) cube([fabric_t,cord_w,fabric_t],center=true);
        translate([15*sin((i+1)*45),0,(i+1)*4]) cube([fabric_t,cord_w,fabric_t],center=true);
    }
}
module link(a,b) { // Segment symbolique du chemin de récupération.
    hull() { translate(a) sphere(d=2,$fn=12); translate(b) sphere(d=2,$fn=12); }
}
module prodat() { cylinder(d=prodat_d,h=prodat_l); }
module assembly() {
    color("Ivory") shell_cut() booster();
    color("OrangeRed") for(a=[0:360/fin_count:359]) rotate([0,0,a])
        translate([body_d/2-fin_embed,0,fin_z]) fin();
    color("BurlyWood") {
        translate([0,0,mount_z]) shell_cut() tube(mount_od,mount_id,mount_l);
        for(z=[aft_ring_z,mid_ring_z,front_ring_z]) translate([0,0,z]) ring();
    }
    color("Silver") translate([body_id/3,0,front_ring_z+ring_t]) eye();
    if(show_motor) translate([0,0,motor_z]) motor();
    if(retention == "MR-1") color("Silver") translate([0,0,aft_ring_z]) retainer();
    translate([0,0,payload_z]) {
        color("Ivory") shell_cut() payload();
        color("Tan") translate([0,0,-coupler_l/2]) shell_cut() coupler();
        color("BurlyWood") translate([0,0,-coupler_l/2]) bulkhead();
        color("Silver") translate([0,0,-coupler_l/2]) rotate([180,0,0]) eye();
    }
    color("OrangeRed") translate([0,0,nose_z]) shell_cut() nose();
    if(show_rail_buttons) color("Black") for(z=rail_z) rotate([0,0,60])
        translate([body_d/2,0,z]) rotate([0,90,0]) rail_button();
    if(show_recovery) {
        color("Tomato") translate([0,0,recovery == "packed" ? pack_z : deploy_z]) parachute();
        if(show_protector) color("Olive")
            translate(recovery == "packed" ? [0,0,pack_z] : [body_d*3,0,pack_z]) protector();
        color("Gold") if(recovery == "packed") translate([-20,0,pack_z]) cord();
        else {
            // Schéma latéral, hors des tubes; ni longueur réelle ni état de vol.
            anchor = [-body_d*2,0,booster_l+100];
            link([body_id/3,0,front_ring_z+ring_t+20],anchor);
            link(anchor,[0,0,payload_z-coupler_l/2-20]);
            link(anchor,[0,0,deploy_z-chute_d/2]);
        }
    }
    if(show_prodat) color("SteelBlue") translate([body_d*2,0,0]) prodat();
}


include <mosaique-generee.scad>
color([0.031,0.165,0.333]) { booster(); translate([0,0,payload_z]) payload();
 translate([0,0,nose_z]) nose();
 for(a=[0:360/fin_count:359]) rotate([0,0,a]) translate([body_d/2-fin_embed,0,fin_z]) fin(); }
if(show_rail_buttons) color("Black") for(z=rail_z) rotate([0,0,60])
 translate([body_d/2,0,z]) rotate([0,90,0]) rail_button();
color("Silver") translate([0,0,aft_ring_z]) retainer();
sillage_mosaique();
