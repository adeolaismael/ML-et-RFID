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
    public class SauvegardesController : Controller
    {
        private readonly PROJETContext _context;

        public SauvegardesController(PROJETContext context)
        {
            _context = context;
        }

        // GET: Sauvegardes
        public async Task<IActionResult> Index()
        {
              return _context.Sauvegarde != null ? 
                          View(await _context.Sauvegarde.ToListAsync()) :
                          Problem("Entity set 'PROJETContext.Sauvegarde'  is null.");
        }

        // GET: Sauvegardes/Details/5
        public async Task<IActionResult> Details(int? id)
        {
            if (id == null || _context.Sauvegarde == null)
            {
                return NotFound();
            }

            var sauvegarde = await _context.Sauvegarde
                .FirstOrDefaultAsync(m => m.IdSauvegarde == id);
            if (sauvegarde == null)
            {
                return NotFound();
            }

            return View(sauvegarde);
        }

        // GET: Sauvegardes/Create
        public IActionResult Create()
        {
            return View();
        }

        // POST: Sauvegardes/Create
        // To protect from overposting attacks, enable the specific properties you want to bind to.
        // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("IdSauvegarde,Accuracy,Heure,methodeId")] Sauvegarde sauvegarde)
        {
            if (ModelState.IsValid)
            {
                _context.Add(sauvegarde);
                await _context.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }
            return View(sauvegarde);
        }

        // GET: Sauvegardes/Edit/5
        public async Task<IActionResult> Edit(int? id)
        {
            if (id == null || _context.Sauvegarde == null)
            {
                return NotFound();
            }

            var sauvegarde = await _context.Sauvegarde.FindAsync(id);
            if (sauvegarde == null)
            {
                return NotFound();
            }
            return View(sauvegarde);
        }

        // POST: Sauvegardes/Edit/5
        // To protect from overposting attacks, enable the specific properties you want to bind to.
        // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, [Bind("IdSauvegarde,Accuracy,Heure,methodeId")] Sauvegarde sauvegarde)
        {
            if (id != sauvegarde.IdSauvegarde)
            {
                return NotFound();
            }

            if (ModelState.IsValid)
            {
                try
                {
                    _context.Update(sauvegarde);
                    await _context.SaveChangesAsync();
                }
                catch (DbUpdateConcurrencyException)
                {
                    if (!SauvegardeExists(sauvegarde.IdSauvegarde))
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
            return View(sauvegarde);
        }

        // GET: Sauvegardes/Delete/5
        public async Task<IActionResult> Delete(int? id)
        {
            if (id == null || _context.Sauvegarde == null)
            {
                return NotFound();
            }

            var sauvegarde = await _context.Sauvegarde
                .FirstOrDefaultAsync(m => m.IdSauvegarde == id);
            if (sauvegarde == null)
            {
                return NotFound();
            }

            return View(sauvegarde);
        }

        // POST: Sauvegardes/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            if (_context.Sauvegarde == null)
            {
                return Problem("Entity set 'PROJETContext.Sauvegarde'  is null.");
            }
            var sauvegarde = await _context.Sauvegarde.FindAsync(id);
            if (sauvegarde != null)
            {
                _context.Sauvegarde.Remove(sauvegarde);
            }
            
            await _context.SaveChangesAsync();
            return RedirectToAction(nameof(Index));
        }

        private bool SauvegardeExists(int id)
        {
          return (_context.Sauvegarde?.Any(e => e.IdSauvegarde == id)).GetValueOrDefault();
        }
    }
}
