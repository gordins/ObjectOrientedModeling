using CodeGenerator.Generators;
using CodeGenerator.Validators;
using Microsoft.AspNetCore.Mvc;
using Model.SchemaModel;

namespace Services.Controllers
{
    [Route("codeGenerator")]
    public class CodeGeneratorController : Controller
    {
        [HttpPost("{language}")]
        public IActionResult GenerateCode(string language, [FromBody] ProcessedText processedText)
        {
            if (language.Equals("json"))
                return Ok(processedText);
            IGenerator generator;
            try
            {
                generator = GeneratorFactory.CreateGenerator(language);
            }
            catch (LanguageNotSupportedException)
            {
                return NotFound();
            }


            if (processedText?.Entities == null)
                return BadRequest();
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            IValidator validator = new SyntaxValidator();
            try
            {
                validator.Validate(processedText);
            }
            catch (SyntaxFlawException e)
            {
                return BadRequest(e.Message + "(" + e.Source + ")");
            }
            validator = new SemanticValidator();
            try
            {
                validator.Validate(processedText);
            }
            catch (SemanticFlawException e)
            {
                return BadRequest(e.Message + "(" + e.Source + ")");
            }

            return Ok(generator.GenerateProcessedText(processedText));
        }
    }
}