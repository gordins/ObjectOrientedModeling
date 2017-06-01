using Microsoft.AspNetCore.Mvc;

namespace Services.Controllers
{
    [Route("")]
    public class MainPage : Controller
    {
        [HttpGet]
        public IActionResult GetMainPage()
        {
            return Ok("Welcome!");
        }
    }
}