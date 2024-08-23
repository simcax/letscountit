CREATE MIGRATION m1yokw6g2b2awl2ox4ws767ewuwteprlulr7tscharfqzbkgtihana
    ONTO m14jpzcdspb2zf4irbgcegjyx47plqkhefnitcarrjj64shitzbaza
{
  ALTER TYPE default::counter {
      ALTER PROPERTY name {
          SET REQUIRED USING (<std::str>{'no name'});
      };
  };
};
