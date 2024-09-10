CREATE MIGRATION m14jpzcdspb2zf4irbgcegjyx47plqkhefnitcarrjj64shitzbaza
    ONTO m1rf4gu7li22oko5n4xxrem7atcewoor7q7kkcevyxeqok4iue4b6q
{
  ALTER TYPE default::counter {
      CREATE PROPERTY count: std::int64 {
          SET default := 0;
      };
  };
};
