using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PROJET.Data;
using PROJET.Models;

namespace PROJET.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class HyperparamètresController : ControllerBase
    {
        private readonly PROJETContext _context;

        public HyperparamètresController(PROJETContext context)
        {
            _context = context;
        }

        // GET: api/Hyperparamètres
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Hyperparamètres>>> GetHyperparamètres()
        {
          if (_context.Hyperparamètres == null)
          {
              return NotFound();
          }
            return await _context.Hyperparamètres.ToListAsync();
        }

        // GET: api/Hyperparamètres/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Hyperparamètres>> GetHyperparamètres(int id)
        {
          if (_context.Hyperparamètres == null)
          {
              return NotFound();
          }
            var hyperparamètres = await _context.Hyperparamètres.FindAsync(id);

            if (hyperparamètres == null)
            {
                return NotFound();
            }

            return hyperparamètres;
        }

        // PUT: api/Hyperparamètres/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutHyperparamètres(int id, Hyperparamètres hyperparamètres)
        {
            if (id != hyperparamètres.IdHParam)
            {
                return BadRequest();
            }

            _context.Entry(hyperparamètres).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!HyperparamètresExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/Hyperparamètres
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<Hyperparamètres>> PostHyperparamètres(Hyperparamètres hyperparamètres)
        {
          if (_context.Hyperparamètres == null)
          {
              return Problem("Entity set 'PROJETContext.Hyperparamètres'  is null.");
          }
            _context.Hyperparamètres.Add(hyperparamètres);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetHyperparamètres", new { id = hyperparamètres.IdHParam }, hyperparamètres);
        }

        // DELETE: api/Hyperparamètres/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteHyperparamètres(int id)
        {
            if (_context.Hyperparamètres == null)
            {
                return NotFound();
            }
            var hyperparamètres = await _context.Hyperparamètres.FindAsync(id);
            if (hyperparamètres == null)
            {
                return NotFound();
            }

            _context.Hyperparamètres.Remove(hyperparamètres);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool HyperparamètresExists(int id)
        {
            return (_context.Hyperparamètres?.Any(e => e.IdHParam == id)).GetValueOrDefault();
        }
    }
}
