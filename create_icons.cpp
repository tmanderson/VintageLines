// Compile and run it with: g++ -I/usr/local/include/cairo create_icons.cpp -lcairo && ./a.out

#include <cairo.h>
#include <stdio.h>
#include <string.h>

void create_pngs(int surfacewidth, int surfaceheight, float fontsize, const char *extension)
{
    cairo_surface_t *surface = cairo_image_surface_create(CAIRO_FORMAT_ARGB32, surfacewidth, surfaceheight);
    cairo_t *cr = cairo_create(surface);

    cairo_select_font_face(cr, "menlo", CAIRO_FONT_SLANT_NORMAL, CAIRO_FONT_WEIGHT_NORMAL);
    cairo_set_font_size(cr, fontsize);
    cairo_text_extents_t extents;
    cairo_text_extents(cr, "0123456789", &extents);

    float fontwidth = extents.width/10; // average character width

    for (int i = 0; i < 100; i++)
    {
        char buf[5];
        sprintf(buf, "%d", i);
        cairo_set_source_rgba (cr, 0, 0, 0, 0);
        cairo_set_operator (cr, CAIRO_OPERATOR_SOURCE);
        cairo_paint (cr);

        cairo_set_source_rgb(cr, 0.75, 0.75, 0.75);
        cairo_move_to(cr, 15-(15-2*fontwidth)-strlen(buf)*fontwidth, fontsize);
        cairo_show_text(cr, buf);
        char file[32] = "icons/";
        strcat(file, buf);
        strcat(file, extension);
        cairo_surface_write_to_png(surface, file);
    }
    cairo_destroy(cr);
    cairo_surface_destroy(surface);
}
int main (int argc, char *argv[])
{
    int width = 14;
    int height = 15;
    float size = 10.0;
    create_pngs(width, height, size, ".png");
    // Apparently 2x gutter icons aren't picked up?
    //create_pngs(width*2, height*2, size*2, "@2x.png");

    return 0;
}
