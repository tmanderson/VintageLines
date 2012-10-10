// Compile and run it with: g++ -I/usr/local/include/cairo create_icons.cpp -lcairo && ./a.out

#include <cairo.h>
#include <stdio.h>
#include <string.h>

#if defined(__MACH__)
#define FONT_FACE "menlo"
#define FONT_SIZE 11.0
#define BRIGHTNESS 0.7
#define HEIGHT 15
#define WIDTH 15
#define PATH "icons/osx/%d.png"
#elif defined(__linux__)
#define FONT_FACE "monospace"
#define FONT_SIZE 12.0
#define BRIGHTNESS 0.60
#define HEIGHT 15
#define WIDTH 14
#define PATH "icons/linux/%d.png"
#else
#define FONT_FACE "consolas"
#define FONT_SIZE 11.0
#define BRIGHTNESS 0.575
#define HEIGHT 15
#define WIDTH 14
#define PATH "icons/windows/%d.png"
#endif

void create_pngs(int surfacewidth, int surfaceheight, float fontsize, const char* format, int start=0, int end=100)
{
    cairo_surface_t *surface = cairo_image_surface_create(CAIRO_FORMAT_ARGB32, surfacewidth, surfaceheight);
    cairo_t *cr = cairo_create(surface);

    cairo_select_font_face(cr, FONT_FACE, CAIRO_FONT_SLANT_NORMAL, CAIRO_FONT_WEIGHT_NORMAL);
    cairo_set_font_size(cr, fontsize);
    cairo_text_extents_t extents;
    cairo_text_extents(cr, "0123456789", &extents);

    float fontwidth = extents.width/10; // average character width

    int chars = 1;
    if (end > 10)
        chars++;
    if (end > 100)
        chars++;
    float align = surfacewidth-chars*fontwidth;

    for (int i = start; i < end; i++)
    {
        char buf[128];
        sprintf(buf, "%d", i);
        cairo_set_source_rgba (cr, 0, 0, 0, 0);
        cairo_set_operator (cr, CAIRO_OPERATOR_SOURCE);
        cairo_paint (cr);

        cairo_set_source_rgb(cr, BRIGHTNESS, BRIGHTNESS, BRIGHTNESS);
        cairo_move_to(cr, surfacewidth-align-strlen(buf)*fontwidth, fontsize);
        cairo_show_text(cr, buf);
        sprintf(buf, format, i);
        cairo_surface_write_to_png(surface, buf);
    }
    cairo_destroy(cr);
    cairo_surface_destroy(surface);
}
int main (int argc, char *argv[])
{
    int width = WIDTH;
    int height = HEIGHT;
    float size = FONT_SIZE;

    create_pngs(width*2, height*2, size*2, PATH);
    return 0;
}
