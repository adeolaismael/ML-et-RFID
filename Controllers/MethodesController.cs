using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using PROJET.Data;
using PROJET.Models;

namespace PROJET.Controllers
{
    public class MethodesController : Controller
    {
        private readonly PROJETContext _context;

        public MethodesController(PROJETContext context)
        {
            _context = context;
        }

        // GET: Methodes
        public async Task<IActionResult> Index()
        {
              return _context.Methode != null ? 
                          View(await _context.Methode.ToListAsync()) :
                          Problem("Entity set 'PROJETContext.Methode'  is null.");
        }

        // GET: Methodes/Details/5
        public async Task<IActionResult> Details(int? id)
        {
            if (id == null || _context.Methode == null)
            {
                return NotFound();
            }

            var methode = await _context.Methode
                .FirstOrDefaultAsync(m => m.Id == id);
            if (methode == null)
            {
                return NotFound();
            }

            return View(methode);
        }

        // GET: Methodes/Create
        public IActionResult Create()
        {
            return View();
        }

        // POST: Methodes/Create
        // To protect from overposting attacks, enable the specific properties you want to bind to.
        // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("Id,Nom,NbrHParam")] Methode methode)
        {
            if (ModelState.IsValid)
            {
                _context.Add(methode);
                await _context.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }
            return View(methode);
        }

        // GET: Methodes/Edit/5
        public async Task<IActionResult> Edit(int? id)
        {
            if (id == null || _context.Methode == null)
            {
                return NotFound();
            }

            var methode = await _context.Methode.FindAsync(id);
            if (methode == null)
            {
                return NotFound();
            }
            return View(methode);
        }

        // POST: Methodes/Edit/5
        // To protect from overposting attacks, enable the specific properties you want to bind to.
        // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, [Bind("Id,Nom,NbrHParam")] Methode methode)
        {
            if (id != methode.Id)
            {
                return NotFound();
            }

            if (ModelState.IsValid)
            {
                try
                {
                    _context.Update(methode);
                    await _context.SaveChangesAsync();
                }
                catch (DbUpdateConcurrencyException)
                {
                    if (!MethodeExists(methode.Id))
                    {
                        return NotFound();
                    }
                    else
                    {
                        throw;
                    }
                }
                return RedirectToAction(nameof(Index));
            }
            return View(methode);
        }

        // GET: Methodes/Delete/5
        public async Task<IActionResult> Delete(int? id)
        {
            if (id == null || _context.Methode == null)
            {
                return NotFound();
            }

            var methode = await _context.Methode
                .FirstOrDefaultAsync(m => m.Id == id);
            if (methode == null)
            {
                return NotFound();
            }

            return View(methode);
        }

        // POST: Methodes/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            if (_context.Methode == null)
            {
                return Problem("Entity set 'PROJETContext.Methode'  is null.");
            }
            var methode = await _context.Methode.FindAsync(id);
            if (methode != null)
            {
                _context.Methode.Remove(methode);
            }
            
            await _context.SaveChangesAsync();
            return RedirectToAction(nameof(Index));
        }

        private bool MethodeExists(int id)
        {
          return (_context.Methode?.Any(e => e.Id == id)).GetValueOrDefault();
        }
    }
}
