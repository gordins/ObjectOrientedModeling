using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;

namespace Model.SchemaModel
{
    public class ProcessedText
    {
        [Required] public List<Entity> Entities = new List<Entity>();

        public Entity RetriveByName(string name)
        {
            var entityToRetrive = Entities.SingleOrDefault(entity => entity.Name == name);
            if (entityToRetrive != null)
                return entityToRetrive;
            var newEntity = new Entity
            {
                Name = name
            };
            Entities.Add(newEntity);
            return newEntity;
        }
    }
}